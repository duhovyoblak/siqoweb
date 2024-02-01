#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask                    import url_for, get_flashed_messages, flash, render_template, make_response
from   flask                    import request, session, abort, redirect
from   flask_login              import login_user
from   markupsafe               import escape

import jinja2                   as j2
from   jinja2                   import Environment, PackageLoader, select_autoescape

import siqo_lib.general         as gen

import siqo_web.dms             as dms
from   siqo_web.forms           import FormLogin
from   siqo_web.user            import User


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_CWD      = os.getcwd()


if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Page
#------------------------------------------------------------------------------
class Page:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, name, env, dtbs, user, height, data="basepage.json", template="_base.html"):
        "Call constructor of Page and initialise it"
        
        journal.I(f"Page({name}).init:")

        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.journal       = journal
        self.name          = name
        self.env           = env

        self.dtbs          = dtbs
        self.user          = user

        self.height        = height
        self.data          = data
        self.template      = template

        #----------------------------------------------------------------------
        # Dynamicke premenne
        #----------------------------------------------------------------------
        self.page          = {}
        self.context       = {}
        self.formLogin     = None
        
        #----------------------------------------------------------------------
        # Nacitanie json data pre page
        #----------------------------------------------------------------------
        fName = f"{os.getcwd()}/static/data/{self.data}"
        self.pageData = gen.loadJson(journal, fileName = fName)

        self.journal.M(f"Page({self.name}).init: data was loaded")

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
    
        self.journal.O(f"Page({self.name}).init")
        
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
        # Ak je POST, vyhodnotim formular
        #----------------------------------------------------------------------
        if self.formLogin.validate_on_submit():
            
            #------------------------------------------------------------------
            # User uz je autentifikovany
            #------------------------------------------------------------------
            if False and flask.current_user.is_authenticated:
                
                self.journal.M(f"{self.name}.resp: login_user...")
                self.journal.O()
                return redirect(url_for('homepage'))

            #------------------------------------------------------------------
            # Autentifikacia usera podla udajov z formulara
            #------------------------------------------------------------------
            user = self.formLogin.username.data
            pasw = self.formLogin.password.data
            rmbr = self.formLogin.remember.data

            if not self.user.authenticate(user, pasw):

                flash('Invalid username or password')
                self.journal.M(f"{self.name}.resp: login_user...")
                self.journal.O()
                return redirect(url_for('homepage'))

            #------------------------------------------------------------------
            # User je autentifikovany, zapisem do session
            #------------------------------------------------------------------
            login_user(self.user, remember=rmbr)

            self.journal.M(f"{self.name}.resp: User logged in")
            self.journal.O()
            return redirect(url_for('homepage'))
 
        #----------------------------------------------------------------------
        # Inak vytvorim HTML stranku pre GET
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
print(f"Page {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
