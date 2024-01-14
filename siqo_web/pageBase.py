#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   flask                    import url_for, render_template, make_response
from   flask                    import request, session, abort, redirect
from   markupsafe               import escape

import jinja2 as j2
from jinja2          import Environment, PackageLoader, select_autoescape

import siqo_web.dms       as dms
from siqo_web.forms       import FormLogin


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_IS_TEST  = True if os.environ['wsiqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Page
#------------------------------------------------------------------------------
class PageBase:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, name, env, template, pageDms):
        "Call constructor of PageBase and initialise it"
        
        self.journal       = journal
        
        self.name          = f"Base_{name}"
        self.env           = env
        self.template      = template
        self.data          = {}
        self.context       = {"url_for":url_for}
        
        #----------------------------------------------------------------------
        self.journal.I(f"{self.name}.init:")
    
        #----------------------------------------------------------------------
        # Nacitanie json data pre page
        #----------------------------------------------------------------------
        self.data = dms.loadJson(pageDms)
        self.journal.M(f"{self.name}.init: {self.data}")

        #----------------------------------------------------------------------
        # Inicializacia contextu
        #----------------------------------------------------------------------
        self.baseContext(self.data)
        
        #----------------------------------------------------------------------
        # Doplnenie formLogin do contextu
        #----------------------------------------------------------------------
        frmLogin = FormLogin()
        
        cont = {"formLogin":frmLogin}
        self.addContext(cont)
    
        self.journal.O()
        
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
    def baseContext(self, data):
        "Creates context from json-encoded selector page"
    
        self.journal.I(f"{self.name}.baseContext:")

        self.context = {"url_for":url_for}

        self.context["title"        ]= data["title"        ]
        self.context["head_title"   ]= data["head_title"   ]
        self.context["head_subtitle"]= data["head_subtitle"]
        self.context["head_comment" ]= data["head_comment" ]
        
        self.context["user"         ]= "guest user"
    
        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.baseContext = {self.context}")
        self.journal.O()

    #--------------------------------------------------------------------------
    def addContext(self, cont):
        
        self.context.update(cont)

    #==========================================================================
    # API for users
    #--------------------------------------------------------------------------
    def resp(self):
     
        self.journal.I(f"{self.name}.resp: {self.template}")
     
        template = self.env.get_template(self.template)
        self.journal.M(f"{self.name}.resp: {template}")
        
        
        resp = make_response(template.render(**self.context), 200)
        resp.headers['X-Something'] = 'A value'
        
        self.journal.O()
        return resp

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"PageBase {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
