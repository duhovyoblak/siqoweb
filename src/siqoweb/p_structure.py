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

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'

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
        super().__init__(journal, userId, classId, objPar='__ROOT__', rMode= 'STRICT', crForm='Y', lvl=5)

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
        # DMS
        #----------------------------------------------------------------------
        self.dms = DMS(self.journal, self)

        #----------------------------------------------------------------------
        # HTML
        #----------------------------------------------------------------------
        self.html = HTML(self.journal, who=self.name, dms=self.dms)

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
        self.idContext = self.loadContent()
        self.addContext(self.idContext)

        #----------------------------------------------------------------------
        # Ak je template staged, tak urcim defaultne nastaveny stage
        #----------------------------------------------------------------------
        
        
        #----------------------------------------------------------------------
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
    def loadPageResource(self):
        "This method returns resources for this page saved in the Database"
        
        self.journal.I(f"{self.classId}.loadPageResource:")
        
        #----------------------------------------------------------------------
        # Nacitanie objektov PAGE
        #----------------------------------------------------------------------
        res = self.objectGet(self.user, objPar='__PAGE__')
        
        #----------------------------------------------------------------------
        # Heads items
        #----------------------------------------------------------------------
        if '__HEAD__' in res.keys() and 'HeadItems' in res['__HEAD__'].keys():
            
            #------------------------------------------------------------------
            # Vsetkym polozkam v Head nastavim prislusny type
            #------------------------------------------------------------------
            for item in res['__HEAD__']['HeadItems']:
                
                if   '1_Title'    in item.keys(): item['1_Title'   ]['TYPE'] = 'HEADTITLE'
                elif '2_SubTitle' in item.keys(): item['2_SubTitle']['TYPE'] = 'HEADSUBTIT'
                elif '3_Comment'  in item.keys(): item['3_Comment' ]['TYPE'] = 'HEADCOMMENT'

        #----------------------------------------------------------------------
        # NavBar items
        #----------------------------------------------------------------------
        if '__NAVB__' not in res.keys()            : res['__NAVB__'] = {}
        if 'NavLinks' not in res['__NAVB__'].keys(): res['__NAVB__']['NavLinks'] = []

        #----------------------------------------------------------------------
        # 0-ta polozka v NavBar je UserItem - ak nie je, potom ho tam vlozim
        #----------------------------------------------------------------------
        if len(res['__NAVB__']['NavLinks'])==0 or 'User' not in res['__NAVB__']['NavLinks'][0].keys():

            userItem = {"User":{"SK":self.userName, "URL":"pgLogin"}}
            res['__NAVB__']['NavLinks'].insert(0, userItem)
            
        #----------------------------------------------------------------------
        # Vsetkym polozkam v NavBar nastavim type=BARMENUITEM
        #----------------------------------------------------------------------
        for item in res['__NAVB__']['NavLinks']:
                
            for itemId, args in item.items():
                args["TYPE"] = "BARMENUITEM"

        #----------------------------------------------------------------------
        # Stage items
        #----------------------------------------------------------------------
        if '__STAG__' in res.keys():
            
            stagePos = 0
            
            #------------------------------------------------------------------
            # Prejdem vsetky stage
            #------------------------------------------------------------------
            for stageId, stageLst in res['__STAG__'].items():
    
                #--------------------------------------------------------------
                # Vyriesim selector v polozke '0_StageName'
                #--------------------------------------------------------------
                if '0_Stage' not in stageLst[0].keys():
                    
                    #----------------------------------------------------------
                    # Ak nie je kluc '0_Stage' v 0-tej polozke listu je to chyba
                    #----------------------------------------------------------
                    self.journal.M(f"{self.name}.loadPageResource: Stage without 'StageName' will be skipped", True)
                    continue

                else:
                    #----------------------------------------------------------
                    # Ak polozka '0_StageName' existuje, doplnim vlastnosti StageSelectora
                    #----------------------------------------------------------
                    stageLst[0]['0_Stage']['TYPE'] = 'STAGESELECTOR'
                    
                    # Pozicia je v kluci POS ako string, prehodim na int
                    stagePos = int(stageLst[0]['0_Stage']['POS'])
                    stageLst[0]['0_Stage']['POS'] = stagePos
                    
                #--------------------------------------------------------------
                # Ak stage conntent obsahuje len 1 item (okrem 0_StageName)
                #--------------------------------------------------------------
                if len(stageLst)-1 == 1:
                            
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
        # Vygenerujem html
        #----------------------------------------------------------------------
        resp = make_response(template.render(**self.context), 200)
        resp.headers['X-Something'] = 'A value'

        self.journal.O()
        return resp

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
        self.context["height"]= self.height
        self.context["initId"]= self.initId
        self.context["lang"  ]= self.lang

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

    page = Structure(journal, env, 'Homepage', 700)
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
