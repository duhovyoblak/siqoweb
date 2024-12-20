#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   flask                 import url_for, get_flashed_messages, flash, render_template, make_response
from   flask                 import request, session, abort, redirect
from   flask_login           import login_user, logout_user, current_user
from   markupsafe            import escape

import jinja2                as j2
from   jinja2                import Environment, FileSystemLoader, select_autoescape

import siqolib.general       as gen

from   o__object             import Object
from   f__form               import FormStruct

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.07'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------


#==============================================================================
# package's methods
#==============================================================================
# Structure
#------------------------------------------------------------------------------
class Structure(Object):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, env, userId, userName, lang, classId, height, template="1 structure.html"):
        "Call constructor of Structure and initialise it"
        
        journal.I(f"Structure({classId}).init:")
        
        #----------------------------------------------------------------------
        # Konstruktor DataStructure
        #----------------------------------------------------------------------
        super().__init__(journal, userId, lang, classId, height=height, rMode= 'STRICT')

        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.name          = f"Struct({self.name})"
        self.template      = template
        self.env           = env
        self.loaded        = False

        self.userName      = userName
        
        self.initId        = "Content"
        self.context       = {}
        

        #----------------------------------------------------------------------
        # Inicializacia statickeho contextu
        #----------------------------------------------------------------------
        self.initContext()

        #----------------------------------------------------------------------
        # Doplnenie statickeho contextu z DB
        #----------------------------------------------------------------------
        self.dbContext = self.loadPageResource()
        self.addContext(self.dbContext)

        #----------------------------------------------------------------------
        #gen.dictPrint(dct=self.context)
        self.journal.O(f"{self.name}.init")
        
    #==========================================================================
    # Vytvorenie page
    #--------------------------------------------------------------------------
#!!!! znacka
    def loadPageResource(self):
        "This method returns resources for this page saved in the Database"
        
        self.journal.I(f"{self.name}.loadPageResource:")
        
        #----------------------------------------------------------------------
        # Nacitanie objektov PAGE {'__HEAD__': {},'__NAVB__': {},'__STAG__': {},'__CONT__': {}}
        #----------------------------------------------------------------------
        res = self.pageGet(self.userId)
        
        #----------------------------------------------------------------------
        # NavBar objects
        #----------------------------------------------------------------------
        userBarLink = {"User":{"SK":self.userName, "URL":"pgLogin", "TYPE":"BARMENUITEM"}}

        #----------------------------------------------------------------------
        # Skontrolujem ci existuje definicia NavBar objects
        #----------------------------------------------------------------------
        if len(res['__NAVB__']) > 0:

            #------------------------------------------------------------------
            # Zistim ako sa vola objekt pre navBarLinks
            #------------------------------------------------------------------
            for navBarObjId, navBarLst in res['__NAVB__'].items():
                
                #--------------------------------------------------------------
                # Vsetkym objektom v NavBarLst nastavim type=BARMENUITEM
                #--------------------------------------------------------------
                for navBarObj in navBarLst:
                
                    #{'1_Admin': {'SK': 'Admin', 'URL': 'pgAdmin'}}
                    key = list(navBarObj.keys())[0]
                    navBarObj[key]["TYPE"] = "BARMENUITEM"

                #--------------------------------------------------------------
                # 0-ta polozka v NavBarLst je UserItem - vlozim ho tam
                #--------------------------------------------------------------
                res['__NAVB__'][navBarObjId].insert(0, userBarLink)
            
        #----------------------------------------------------------------------
        # NavBar nedefinovany, vlozim usera
        #----------------------------------------------------------------------
        else: res['__NAVB__'] = {'NavLinks': [userBarLink]}

        #----------------------------------------------------------------------
        # Stage objects
        #----------------------------------------------------------------------
        if '__STAG__' in res.keys():
            
            stagePos = 0
            
            #------------------------------------------------------------------
            # Prejdem vsetky stage
            #------------------------------------------------------------------
            for stageObj, stageLst in res['__STAG__'].items():
    
                #--------------------------------------------------------------
                # Vyriesim selector v [0]-tej polozke s klucom '0_Stage'
                #--------------------------------------------------------------
                if '0_Stage' not in stageLst[0].keys():
                    
                    #----------------------------------------------------------
                    # Ak nie je kluc '0_Stage' v 0-tej polozke listu je to chyba
                    #----------------------------------------------------------
                    self.journal.M(f"{self.name}.loadPageResource: Stage without '0_Stage' will be skipped", True)
                    continue

                else:
                    #----------------------------------------------------------
                    # Ak polozka '0_Stage' existuje, doplnim vlastnosti StageSelectora
                    #----------------------------------------------------------
                    stageLst[0]['0_Stage']['TYPE'] = 'STAGESELECTOR'
                    
                    # Pozicia je v kluci POS ako string, prehodim na int
                    stagePos = int(stageLst[0]['0_Stage']['POS'])
                    stageLst[0]['0_Stage']['POS'] = stagePos
                    
                #--------------------------------------------------------------
                # Ak stage conntent nie je definovany
                #--------------------------------------------------------------
                if len(stageLst)-1 == 0:

                    self.journal.M(f"{self.name}.loadPageResource: Stage {stageObj} has no content defined", True)

                #--------------------------------------------------------------
                # Ak stage conntent obsahuje len 1 item (okrem 0_StageName)
                #--------------------------------------------------------------
                elif len(stageLst)-1 == 1:
                            
                    itemId = list(stageLst[1].keys())[0]
                            
                    if 'TYPE' not in  stageLst[1][itemId].keys(): typeStash = 'P'
                    else: typeStash = stageLst[1][itemId]['TYPE']
                            
                    stageLst[1][itemId]['TYPE'     ] = 'STAGEBOTH'
                    stageLst[1][itemId]['typeStash'] = typeStash
                    stageLst[1][itemId]['POS'      ] = stagePos
                        
                #--------------------------------------------------------------
                # Ak stage conntent obsahuje viac items
                #--------------------------------------------------------------
                else:
                    #----------------------------------------------------------
                    # Prvy item zmenim na 'STAGESTART'
                    #----------------------------------------------------------
                    itemId = list(stageLst[1].keys())[0]

                    if 'TYPE' not in  stageLst[1][itemId].keys(): typeStash = 'P'
                    else: typeStash = stageLst[1][itemId]['TYPE']
                            
                    stageLst[1][itemId]['TYPE'     ] = 'STAGESTART'
                    stageLst[1][itemId]['typeStash'] = typeStash
                    stageLst[1][itemId]['POS'      ] = stagePos
                        
                    #----------------------------------------------------------
                    # Posledny item zmenim na 'STAGESTOP'
                    #----------------------------------------------------------
                    itemId = list(stageLst[-1].keys())[0]

                    if 'TYPE' not in  stageLst[-1][itemId].keys(): typeStash = 'P'
                    else: typeStash = stageLst[-1][itemId]['TYPE']
                            
                    stageLst[-1][itemId]['TYPE'     ] = 'STAGESTOP'
                    stageLst[-1][itemId]['typeStash'] = typeStash
                    stageLst[-1][itemId]['POS'      ] = stagePos

            #------------------------------------------------------------------
            # Prekodujem vsetky Stage do poradia urceneho POS
            #------------------------------------------------------------------
            posLst = []
            
            #------------------------------------------------------------------
            # Ziskam list tuples [(stageId, pos)]
            #------------------------------------------------------------------
            for stageId, stageLst in res['__STAG__'].items():
                                         
                if '0_Stage' not in stageLst[0].keys():
                    
                    #----------------------------------------------------------
                    # Ak nie je kluc '0_Stage' v 0-tej polozke listu je to chyba
                    #----------------------------------------------------------
                    self.journal.M(f"{self.name}.loadPageResource: Stage without 'StageName' will be skipped", True)
                    continue

                else:
                    posLst.append( (stageId, stageLst[0]['0_Stage']['POS']) )
                
            #------------------------------------------------------------------
            # Zosortujem list podla POS
            #------------------------------------------------------------------
            posLst.sort( key=lambda tupl: tupl[1] )
            
            #------------------------------------------------------------------
            # Prekodujem vsetky Stage podla sorted posLst
            #------------------------------------------------------------------
            copySTAG = res['__STAG__']
            
            res['__STAG__'] = {}
            
            for stageTuple in posLst:
                
                res['__STAG__'][stageTuple[0]] = copySTAG[stageTuple[0]]
                
            #------------------------------------------------------------------
        #----------------------------------------------------------------------
        self.loaded = True
        self.journal.M(f"{self.name}.loadPageResource: {gen.dictString(res)}")
        
        #----------------------------------------------------------------------
        self.journal.O()
        return res
    
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def pageGet(self, who):
        """"Returns dict of default objects {'objDefId': { 'objId':[<items>] } }"""
        
        self.journal.I(f"{self.name}.pageGet: For page '{self.classId}'")

        #----------------------------------------------------------------------
        # Inicializacia default objektov
        #----------------------------------------------------------------------
        toRet = {'__HEAD__': {}
                ,'__NAVB__': {}
                ,'__STAG__': {}
                ,'__CONT__': {}
                }
        
        #----------------------------------------------------------------------
        # Prehladanie objektov pre parenta parId a objektu objId
        #----------------------------------------------------------------------
        for parId in toRet.keys():

            #------------------------------------------------------------------
            # Pokusim sa ziskat vnorene objekty
            #------------------------------------------------------------------
            inObjs = self.objectGet(who, objPar=parId)
                
            #------------------------------------------------------------------
            # Ak existuju vnorene objekty, tak ich vlozim
            #------------------------------------------------------------------
            if len(inObjs) > 0: toRet[parId] = inObjs
            else              : self.journal.M(f"{self.name}.pageGet: '{parId}' has no children objects")

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    # Context methods
    #--------------------------------------------------------------------------
    def initContext(self):
        "Creates context"
    
        self.journal.I(f"{self.name}.initContext:")
        self.context = {}

        #----------------------------------------------------------------------
        # Funkcie
        #----------------------------------------------------------------------
        self.context["len"                 ] = len
        self.context["url_for"             ] = url_for
        self.context["get_flashed_messages"] = get_flashed_messages
        self.context["html"                ] = self.html
        
        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.context["height"              ] = self.height
        self.context["initId"              ] = self.initId
        self.context["lang"                ] = self.lang

        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.initContext: Context initialised")
        self.journal.O()

    #--------------------------------------------------------------------------
    def addContext(self, cont):
        "Add optional context"
        
        self.journal.I(f"{self.name}.addContext: {cont.keys()}")
        self.context.update(cont)
        self.journal.O()

    #--------------------------------------------------------------------------
    def addFlash(self, mess):

        self.journal.I(f"{self.name}.addFlash: {mess}")
        flash(mess)
        self.journal.O()

    #--------------------------------------------------------------------------
    def setInitId(self, initId):

        self.journal.I(f"{self.name}.initId: {initId}")
        
        self.initId = initId
        self.addContext({"initId":self.initId})
         
        self.journal.O()

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal                 import SiqoJournal
    journal = SiqoJournal('test-Structure', debug=5)
    
    env = Environment(
     autoescape = select_autoescape()
    ,loader     = FileSystemLoader(['templates'])

    )
    
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'PagManLogin', 700)
    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'PagManHomepage', 700)
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'FAQ', 700)
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'OHISTORY', 700)
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'PagManContact', 700)
 
    rec = page.context

#    item = page.dms.loadForumItem('ja', forumId='OHISTORY')

    
#==============================================================================
print(f"Structure {_VER}")

"""
for stageId, stage in page.context['__STAG__']['objs'].items():

    print(stageId)

    for objId, obj in stage['objs'].items():

        if objId.startswith('SName'): print('selector ', objId, ', items ', obj['items'])
        if objId.startswith('SCont'): print('content ',  objId, ', items ', obj['items'])
"""

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
