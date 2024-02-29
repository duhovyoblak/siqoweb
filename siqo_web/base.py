#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask                    import url_for, get_flashed_messages, flash, render_template, make_response
from   flask                    import request, session, abort, redirect
from   flask_login              import login_user, logout_user, current_user
from   markupsafe               import escape

import jinja2                   as j2
from   jinja2                   import Environment, PackageLoader, select_autoescape

import siqo_lib.general         as gen

from   siqo_web.config          import Config
from   siqo_web.dms             import DMS
from   siqo_web.html            import HTML
from   siqo_web.user            import User
from   siqo_web.object          import Object
from   siqo_web.forms           import FormLogin


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.00'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------


#==============================================================================
# package's methods
#==============================================================================
# Base
#------------------------------------------------------------------------------
class Base(Object):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, env, classId, height, template="base.html"):
        "Call constructor of Base and initialise it"
        
        journal.I(f"Base({classId}).init:")
        
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
        # Konstruktor Database
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
        journal.M(f"Base({self.classId}).init: user = '{userName}'")
        journal.M(f"Base({self.classId}).init: lang = '{self.lang}'")

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
        # Doplnenie dynamickeho contextu
        #----------------------------------------------------------------------
        self.classIdRes   = self.loadPageResource()
        self.addContext(self.classIdRes)

        self.cont   = self.loadContent()
        self.addContext(self.cont)

        #----------------------------------------------------------------------
        # Extra class members
        #----------------------------------------------------------------------
        self.extra  = self.loadExtra()
        self.addContext(self.extra)
        
        self.journal.O(f"Base({self.name}).init")
        
    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadExtra(self):
        
        self.journal.I(f"{self.classId}.initExtra:")
        
        self.journal.O()
        return {}
 
    #--------------------------------------------------------------------------
    def loadContent(self):
        
        self.journal.I(f"{self.classId}.loadContent:")
        
        self.journal.O()
        return {'__CONT__':{}}

    #--------------------------------------------------------------------------
    def loadPageResource(self):
        
        self.journal.I(f"{self.classId}.loadPageResource:")
        
        #----------------------------------------------------------------------
        # Nacitanie objektov PAGE
        #----------------------------------------------------------------------
        res   = self.objectGet(self.user, objPar='__PAGE__')
        
        toRet = {'__HEAD__':{}, '__NAVB__':{}, '__STAG__':{}}
        
        #----------------------------------------------------------------------
        # Heads items
        #----------------------------------------------------------------------
        if '__HEAD__' in res.keys() and 'items' in res['__HEAD__'].keys():
            
            #------------------------------------------------------------------
            # Vsetkym polozkam v Head nastavim prislusny type
            #------------------------------------------------------------------
            for item in res['__HEAD__']['items']:
                
                if   '1_Title'    in item.keys(): item['1_Title'   ]['TYPE'] = 'HEADTITLE'
                elif '2_SubTitle' in item.keys(): item['2_SubTitle']['TYPE'] = 'HEADSUBTIT'
                elif '3_Comment'  in item.keys(): item['3_Comment' ]['TYPE'] = 'HEADCOMMENT'

        #----------------------------------------------------------------------
        # NavBar items
        #----------------------------------------------------------------------
        if '__NAVB__' in res.keys() and 'items' in res['__NAVB__'].keys():

            #------------------------------------------------------------------
            # 0-ta polozka v NavBar je UserItem - ak nie je, potom ho tam vlozim
            #------------------------------------------------------------------
            if len(res['__NAVB__']['items'])==0 or 'User' not in res['__NAVB__']['items'][0].keys():

                userItem = {"User":{"SK":self.userName, "URL":"login"}}
                res['__NAVB__']['items'].insert(0, userItem)
            
            #------------------------------------------------------------------
            # Vsetkym polozkam v NavBar nastavim type=BARMENUITEM
            #------------------------------------------------------------------
            for item in res['__NAVB__']['items']:
                
                for itemId, args in item.items():
                    args["TYPE"] = "BARMENUITEM"

        #----------------------------------------------------------------------
        # Stage items
        #----------------------------------------------------------------------
        if '__STAG__' in res.keys() and 'objs' in res['__STAG__'].keys():
            
            #------------------------------------------------------------------
            # Prejdem vsetky stage
            #------------------------------------------------------------------
            for stageId, stage in res['__STAG__']['objs'].items():
    
                # Pozicia stage je definovana v 0-tom items v argumente POS
                pos = stage['items'][0]['StagePos']['POS']
    
                #--------------------------------------------------------------
                # V stage su dva objekty: SName a SCont
                #--------------------------------------------------------------
                for objId, obj in stage['objs'].items():
        
                    if objId.startswith('SName'):
            
                        #------------------------------------------------------
                        # Vsetkym itemom v Selectore doplnim typ a poziciu
                        #------------------------------------------------------
                        for item in obj['items']:
                            
                            for itemId, args in item.items():
                                args['TYPE'] = 'STAGESELECTOR'
                                args['pos' ] = pos
                            
                    else:
                        print(obj['items'])
                        #------------------------------------------------------
                        # Ak stage conntent obsahuje len 1 item
                        #------------------------------------------------------
                        if len(obj['items']) == 1:
                            
                            itemId = list(obj['items'][0].keys())[0]
                            
                            if 'TYPE' not in  obj['items'][0][itemId].keys(): typeStash = 'P'
                            else: typeStash = obj['items'][0][itemId]['TYPE']
                            
                            obj['items'][0][itemId]['TYPE'     ] = 'STAGEBOTH'
                            obj['items'][0][itemId]['typeStash'] = typeStash
                            obj['items'][0][itemId]['pos'      ] = pos
                        
                        else:
                        #------------------------------------------------------
                        # Prvy item zmenim na 'STAGESTART'
                        #------------------------------------------------------

                            itemId = list(obj['items'][0].keys())[0]

                            if 'TYPE' not in  obj['items'][0][itemId].keys(): typeStash = 'P'
                            else: typeStash = obj['items'][0][itemId]['TYPE']
                            
                            obj['items'][0][itemId]['TYPE'     ] = 'STAGESTART'
                            obj['items'][0][itemId]['typeStash'] = typeStash
                            obj['items'][0][itemId]['pos'      ] = pos
                        
                        #------------------------------------------------------
                        # Posledny item zmenim na 'STAGESTOP'
                        #------------------------------------------------------

                            itemId = list(obj['items'][-1].keys())[0]

                            if 'TYPE' not in  obj['items'][-1][itemId].keys(): typeStash = 'P'
                            else: typeStash = obj['items'][-1][itemId]['TYPE']
                            
                            obj['items'][-1][itemId]['TYPE'     ] = 'STAGESTOP'
                            obj['items'][-1][itemId]['typeStash'] = typeStash
                            obj['items'][-1][itemId]['pos'      ] = pos

                #--------------------------------------------------------------
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
        self.addContext({"initId":initId})
        self.journal.O()

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqo_lib                 import SiqoJournal
    journal = SiqoJournal('test-base', debug=5)
    
    env = Environment(
    
     autoescape = select_autoescape()
    ,loader     = PackageLoader(package_name="siqo_web", package_path="templates")
    )

    page = Base(journal, env, 'Homepage', 700)
    rec = page.context
    
#==============================================================================
print(f"Base {_VER}")

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
