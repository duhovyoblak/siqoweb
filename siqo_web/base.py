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

from   siqo_web.database        import Database
from   siqo_web.config          import Config
from   siqo_web.user            import User
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
class Base(Database):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, name, env, height, template="base.html"):
        "Call constructor of Base and initialise it"
        
        journal.I(f"Base({name}).init:")

        #----------------------------------------------------------------------
        # Konstruktor Database
        #----------------------------------------------------------------------
        super().__init__(journal, Config.dtbsName, Config.dtbsPath)

        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.journal       = journal
        self.name          = name
        self.resTable      = Config.dtbsRes
        self.loaded        = False
        self.env           = env
        self.template      = template
        self.height        = height
        self.initId        = "Content"
        self.context       = {}
        
        #----------------------------------------------------------------------
        # Aktualny user a jazyk
        #----------------------------------------------------------------------
        self.lang = 'SK'
        self.user = current_user
        journal.M(f"Base({name}).init: user = '{self.user}'")

        #----------------------------------------------------------------------
        # Inicializacia statickeho contextu
        #----------------------------------------------------------------------
        self.initContext()

        #----------------------------------------------------------------------
        # Doplnenie dynamickeho contextu
        #----------------------------------------------------------------------
        self.page   = self.loadPage()
        self.addContext(self.page)

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
        
        self.journal.I(f"{self.name}.initExtra:")
        
        self.journal.O()
        return {}
 
    #--------------------------------------------------------------------------
    def loadContent(self):
        
        self.journal.I(f"{self.name}.loadContent:")
        
        self.journal.O()
        return {'content':[{'key':'val'}]}

    #--------------------------------------------------------------------------
    def loadPage(self):
        
        self.journal.I(f"{self.name}.loadPage:")
        
        sql = f"""SELECT S_KEY, S_VAL, C_TYPE FROM {self.resTable} 
                  WHERE 
                  PAGE_ID = '{self.name}' AND OBJ_ID = '__PAGE__' AND LANG_ID = '{self.lang}'"""
        
        rows = self.readDb(self.name, sql)
        
        #----------------------------------------------------------------------
        # Skontrolujem existenciu dat
        #----------------------------------------------------------------------
        if type(rows)==int:
            
            self.loaded = False
            self.journal.M(f"{self.name}.loadPage: Method failed", True)
            self.journal.O()
            return None
        
        #----------------------------------------------------------------------
        # Skonvertujem data
        #----------------------------------------------------------------------
        dic = {}
        
        for row in rows:
            dic[row[0]] = row[1]
        
        #----------------------------------------------------------------------
        self.loaded = True
        self.journal.O()
        return {'page':dic}
    
    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost: Default None post response")
        
        self.journal.O()
        return None

    #--------------------------------------------------------------------------
    def respGet(self):
     
        self.journal.I(f"{self.name}.respGet: Default html get response from template='{self.template}'")
        
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
     
        self.journal.I(f"{self.name}.resp:")
        
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
    
        self.journal.I(f"{self.name}.renderItem:")

        toRet = ""
    
        toRet = item
    
        self.journal.O()
        return toRet
    
    #--------------------------------------------------------------------------
    def initContext(self):
        "Creates context"
    
        self.journal.I(f"{self.name}.initContext:")
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
        self.addContext({"initId":initId})
        self.journal.O()

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"Base {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
