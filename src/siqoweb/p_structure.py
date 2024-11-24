#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask             import url_for, get_flashed_messages, flash, render_template, make_response
from   flask             import request, session, abort, redirect
from   flask_login       import login_user, logout_user, current_user
from   markupsafe        import escape

import jinja2            as j2
from   jinja2            import Environment, FileSystemLoader, select_autoescape

import siqolib.general   as gen

from   app_dms           import DMS
from   html_render       import HTML
from   object            import Object
from   f_form            import FormStruct

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.05'

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
    def __init__(self, journal, env, classId, height, template="1 structure.html"):
        "Call constructor of Structure and initialise it"
        
        journal.I(f"Structure({classId}).init:")
        
        #----------------------------------------------------------------------
        # Identifikacia usera
        #----------------------------------------------------------------------
        user = current_user
        
        if user is not None and str(user)[:5]=='User>': 
            
            userId   = user.user_id
            userName = user.userName()
            lang     = user.lang_id
            
        else: 
            userId   = 'Anonymous'
            userName = 'Guest User'
            lang     = 'SK'

        #----------------------------------------------------------------------
        # Konstruktor DataStructure
        #----------------------------------------------------------------------
        super().__init__(journal, userId, classId, objPar='__ROOT__', rMode= 'STRICT')

        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.journal       = journal
        self.loaded        = False
        self.env           = env
        
        self.userName      = userName
        self.lang          = lang
        self.template      = template
        self.height        = height
        
        self.initId        = "Content"
        self.context       = {}
        
        #----------------------------------------------------------------------
        # Aktualny user a jazyk
        #----------------------------------------------------------------------
        journal.M(f"Structure({self.classId}).init: user = '{userName}'")
        journal.M(f"Structure({self.classId}).init: lang = '{self.lang}'")

        #----------------------------------------------------------------------
        # Vytvorenie DMS a HTM renderera
        #----------------------------------------------------------------------
        self.dms  = DMS (self.journal, self)
        self.html = HTML(self.journal, who=self.name, dms=self.dms, classId=classId)

        #----------------------------------------------------------------------
        # Inicializacia statickeho contextu
        #----------------------------------------------------------------------
        self.initContext()

        #----------------------------------------------------------------------
        # Doplnenie dynamickeho contextu z DB
        #----------------------------------------------------------------------
        self.dbContext = self.loadPageResource()
        self.addContext(self.dbContext)

        #----------------------------------------------------------------------
        # Doplnenie specifickeho contextu z DB podla id
        #----------------------------------------------------------------------
#        self.idContext = self.loadContent()
#        self.addContext(self.idContext)
       
        #----------------------------------------------------------------------
        # Doplnenie defaultneho formulara
        #----------------------------------------------------------------------
#        self.formStruct = FormStruct()
#        self.addContext({'formStruct':self.formStruct})

        #----------------------------------------------------------------------
        #gen.dictPrint(dct=self.context)
        self.journal.O(f"Structure({self.name}).init")
        
    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadContent(self):
        "This method should return page specific content like forms, objects etc."
        
        self.journal.I(f"{self.classId}.loadContent:")
        
        self.journal.O()
        return {'__CONT__':{}}

    #--------------------------------------------------------------------------
#!!!! znacka
    def loadPageResource(self):
        "This method returns resources for this page saved in the Database"
        
        self.journal.I(f"{self.classId}.loadPageResource:")
        
        #----------------------------------------------------------------------
        # Nacitanie objektov PAGE
        #----------------------------------------------------------------------
        res = self.pageGet(self.user)
        
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
    # Response generators
    #--------------------------------------------------------------------------
    def resp(self):
     
        self.journal.I(f"{self.classId}.resp:")
        
        #----------------------------------------------------------------------
        # Skontrolujem stav stranky, vyskocim ak nie je pripravena
        #----------------------------------------------------------------------
        if not self.loaded:
            self.journal.O()
            abort(500)
        
        #----------------------------------------------------------------------
        # POST Method: Vyhodnotim formulare
        #----------------------------------------------------------------------
        if request.method == 'POST':
            
            resp = self.respPost()
            
            #------------------------------------------------------------------
            # Ak je POST response validna
            #------------------------------------------------------------------
            if resp is not None:
                self.journal.O()
                return resp

        #----------------------------------------------------------------------
        # Default response: Ziskam template a vratim html
        #----------------------------------------------------------------------
        resp = self.respGet()
        self.journal.O()
        return resp

    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.classId}.respPost: Default None post response")
        
        
        
        
        self.journal.O()
        return None

    #--------------------------------------------------------------------------
    def respGet(self):
     
        self.journal.I(f"{self.classId}.respGet: Default html get response from template='{self.template}'")
        
        template = self.env.get_template(self.template)
        self.journal.M(f"{self.name}.resp: template loaded")

        #----------------------------------------------------------------------
        # Vygenerujem html response
        #----------------------------------------------------------------------
        resp = make_response(template.render(**self.context), 200)
        resp.headers['X-Something'] = 'A value'

        self.journal.O()
        return resp

    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    # Context methods
    #--------------------------------------------------------------------------
    def initContext(self):
        "Creates context"
    
        self.journal.I(f"{self.classId}.initContext:")
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
        # Navigation Bar
        #----------------------------------------------------------------------
        if str(self.user).startswith("User>"): self.context["userName"]= self.user.userName()
        else                                 : self.context["userName"]= 'Guest User'
        
        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.initContext: Context initialised")
        self.journal.O()

    #--------------------------------------------------------------------------
    def addContext(self, cont):
        "Add optional context"
        
        self.journal.I(f"{self.classId}.addContext: {cont.keys()}")
        self.context.update(cont)
        self.journal.O()

    #--------------------------------------------------------------------------
    def addFlash(self, mess):

        self.journal.I(f"{self.classId}.addFlash: {mess}")
        flash(mess)
        self.journal.O()

    #--------------------------------------------------------------------------
    def setInitId(self, initId):

        self.journal.I(f"{self.classId}.initId: {initId}")
        
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

#    page = Structure(journal, env, 'PagManLogin', 700)
#    page = Structure(journal, env, 'PagManHomepage', 700)
#    page = Structure(journal, env, 'FAQ', 700)
#    page = Structure(journal, env, 'OHISTORY', 700)
    page = Structure(journal, env, 'PagManContact', 700)
 
    rec = page.context
    
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
