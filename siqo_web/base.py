#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   flask                    import url_for, get_flashed_messages, flash, render_template, make_response
from   flask                    import request, session, abort, redirect
from   markupsafe               import escape

import jinja2 as j2
from jinja2          import Environment, PackageLoader, select_autoescape

import siqo_lib.general   as gen
import siqo_web.dms       as dms
from siqo_web.forms       import FormLogin


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_CWD      = os.getcwd()
_IS_TEST  = True if os.environ['wsiqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Page
#------------------------------------------------------------------------------
class Base:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, name, env, height, data="basepage.json", template="_base.html"):
        "Call constructor of Base and initialise it"
        
        journal.I(f"Base({name}).init:")

        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.journal       = journal
        self.name          = name
        self.env           = env
        self.height        = height
        self.data          = data
        self.template      = template

        #----------------------------------------------------------------------
        # Dynamicke premenne
        #----------------------------------------------------------------------
        self.pageData      = {}
        self.context       = {}
        self.formLogin     = None
        
        #----------------------------------------------------------------------
        # Nacitanie json data pre page
        #----------------------------------------------------------------------
        fName = f"{os.getcwd()}/static/data/{self.data}"
        self.pageData = gen.loadJson(journal, fileName = fName)

        self.journal.M(f"Base({self.name}).init: data was loaded")

        #----------------------------------------------------------------------
        # Inicializacia contextu
        #----------------------------------------------------------------------
        self.baseContext(self.pageData)
        
        #----------------------------------------------------------------------
        # Doplnenie formLogin do contextu
        #----------------------------------------------------------------------
        self.formLogin = FormLogin()
        
        cont = {"formLogin":self.formLogin}
        self.addContext(cont)
    
        self.journal.O(f"Base({self.name}).init")
        
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def baseContext(self, data):
        "Creates context from json-encoded selector page"
    
        self.journal.I(f"{self.name}.baseContext:")
        self.context = {}

        #----------------------------------------------------------------------
        # Funkcie
        #----------------------------------------------------------------------
        self.context["len"                 ]= len
        self.context["url_for"             ]= url_for
        self.context["get_flashed_messages"]= get_flashed_messages
        
        #----------------------------------------------------------------------
        # Premenne
        #----------------------------------------------------------------------
        self.context["height"       ]= self.height
        self.context["title"        ]= data["title"        ]
        self.context["head_title"   ]= data["head_title"   ]
        self.context["head_subtitle"]= data["head_subtitle"]
        self.context["head_comment" ]= data["head_comment" ]
        
        self.context["initId"       ]="Content"
        self.context["user"         ]= "guest user"
    
        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.baseContext: Context created")
        self.journal.O()

    #--------------------------------------------------------------------------
    def addContext(self, cont):
        
        self.journal.I(f"{self.name}.addContext:")
        self.context.update(cont)
        self.journal.O()

    #--------------------------------------------------------------------------
    def addFlash(self, mess):

        self.journal.I(f"{self.name}.addFlash: {mess}")
        flash(mess)
        self.journal.O()

    #--------------------------------------------------------------------------
    def renderItem(self, item):
        "Returns HTML for json-encoded item"
    
        self.journal.I(f"{self.name}.renderItem:")

        toRet = ""
    
        toRet = item
    
        self.journal.O()
        return toRet
    
    #==========================================================================
    # API for users
    #--------------------------------------------------------------------------
    def resp(self):
     
        self.journal.I(f"{self.name}.resp: template='{self.template}'")
     
        #----------------------------------------------------------------------
        # Vyhodnotim POST volanie
        #----------------------------------------------------------------------
        if self.formLogin.validate_on_submit():
            
            self.journal.M(f"{self.name}.resp: values in form are valid")

            user = self.formLogin.username.data
            pasw = self.formLogin.password.data
            rmbr = self.formLogin.remember.data
            
            self.addFlash(f"Login requested for user '{user}'({pasw}), remember={rmbr}")

            self.journal.O()
            return redirect('/homepage')
    
        #----------------------------------------------------------------------
        # Vytvorim HTML stranku pre GET
        #----------------------------------------------------------------------
        template = self.env.get_template(self.template)
        self.journal.M(f"{self.name}.resp: template loaded")

        #----------------------------------------------------------------------
        # Vygeneruje page html
        #----------------------------------------------------------------------
        resp = make_response(template.render(**self.context), 200)
        resp.headers['X-Something'] = 'A value'
        
        self.journal.O()
        return resp

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"Base {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
