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

import siqo_web.dms             as dms

from   siqo_web.config          import Config
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
# Base
#------------------------------------------------------------------------------
class Base(Object):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, page, env, height, template="base.html"):
        "Call constructor of Base and initialise it"
        
        journal.I(f"Base({page}).init:")
        
        user = current_user
        print(type(user), ', ', user)
        
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
        super().__init__(journal, page, userId, objPar='__ROOT__', rMode= 'STRICT', crForm='Y', lvl=5)

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
        journal.M(f"Base({self.page}).init: user = '{self.user}'")

        #----------------------------------------------------------------------
        # Inicializacia statickeho contextu
        #----------------------------------------------------------------------
        self.initContext()

        #----------------------------------------------------------------------
        # Doplnenie dynamickeho contextu
        #----------------------------------------------------------------------
        self.pageRes   = self.loadPageResource()
        self.addContext(self.pageRes)

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
        
        self.journal.I(f"{self.page}.initExtra:")
        
        self.journal.O()
        return {}
 
    #--------------------------------------------------------------------------
    def loadContent(self):
        
        self.journal.I(f"{self.page}.loadContent:")
        
        self.journal.O()
        return {'content':[{'key':'val'}]}

    #--------------------------------------------------------------------------
    def loadPageResource(self):
        
        self.journal.I(f"{self.page}.loadPageResource:")
        
        res = self.objectGet(self.user)
        
        #----------------------------------------------------------------------
        # Default polozka v NavBar je User
        #----------------------------------------------------------------------
        if 'res' not in res['__NAVB__'].keys(): res['__NAVB__']['res'] = {}

        if 'User' not in res['__NAVB__']['res'].keys():
            
            #------------------------------------------------------------------
            # Polozku 'User' umiestnim na zaciatok dict a doplnim z res['__NAVB__']['res']
            #------------------------------------------------------------------
            dic = {"User":{"SK":self.userName, "URL":"login"}}
            
            for key, val in res['__NAVB__']['res'].items():
                dic[key] = val
            
            #------------------------------------------------------------------
            # Resource s doplnenym 'User' vratim do res['__NAVB__']['res']
            #------------------------------------------------------------------
            res['__NAVB__']['res'] = dic
        
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
     
        self.journal.I(f"{self.page}.respPost: Default None post response")
        
        self.journal.O()
        return None

    #--------------------------------------------------------------------------
    def respGet(self):
     
        self.journal.I(f"{self.page}.respGet: Default html get response from template='{self.template}'")
        
        template = self.env.get_template(self.template)
        self.journal.M(f"{self.name}.resp: template loaded")

        #----------------------------------------------------------------------
        # Vygenerujem html
        #----------------------------------------------------------------------
        print(self.context)
        resp = make_response(template.render(**self.context), 200)
        resp.headers['X-Something'] = 'A value'

        self.journal.O()
        return resp

    #--------------------------------------------------------------------------
    def resp(self):
     
        self.journal.I(f"{self.page}.resp:")
        
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
    def renderItem(self, item):
        "Returns HTML for json-encoded item"
    
        self.journal.I(f"{self.page}.renderItem:")

        toRet = ""
    
        toRet = item
    
        self.journal.O()
        return toRet
    
    #--------------------------------------------------------------------------
    def initContext(self):
        "Creates context"
    
        self.journal.I(f"{self.page}.initContext:")
        self.context = {}

        #----------------------------------------------------------------------
        # Funkcie
        #----------------------------------------------------------------------
        self.context["len"                 ]= len
        self.context["url_for"             ]= url_for
        self.context["get_flashed_messages"]= get_flashed_messages
        
        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.context["height"       ]= self.height
        self.context["initId"       ]= self.initId
        self.context["lang"         ]= self.lang

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
        
        self.journal.I(f"{self.page}.addContext: {cont.keys()}")
        self.context.update(cont)
        self.journal.O()

    #--------------------------------------------------------------------------
    def addFlash(self, mess):

        self.journal.I(f"{self.page}.addFlash: {mess}")
        flash(mess)
        self.journal.O()

    #--------------------------------------------------------------------------
    def setInitId(self, initId):

        self.journal.I(f"{self.page}.initId: {initId}")
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

    page = Base(journal, 'Homepage', env, 700)
    
#==============================================================================
print(f"Base {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
