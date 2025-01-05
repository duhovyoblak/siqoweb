#==============================================================================
#                                                     (c) SIQO 24
# Class Login for SIQO Flask application
#
#------------------------------------------------------------------------------
import re
import traceback

from   datetime                 import date
from   flask                    import request, session, abort, redirect, flash
from   flask_login              import login_user, logout_user, current_user

from   app_user                 import User, _ANONYM
from   w__window                import Window
from   w_login_f                import LoginForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.11'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
#journal = None
#db      = None

#==============================================================================
# Class Login
#------------------------------------------------------------------------------
class Login(Window):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dms, userId, lang, item, POST, idx):

        journal.I(f"Login.__init__: From {item} for {userId}")

        #----------------------------------------------------------------------
        # Inicializacia Window
        #----------------------------------------------------------------------
        super().__init__(journal, dms, userId, lang, item, POST, idx)

        self.winClass  = 'Login'        # Window's class for response generator

        self.journal.O()

    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost:")
        
        #----------------------------------------------------------------------
        # Continue as Guest User
        #----------------------------------------------------------------------
        if self.form.btnGuest.data:
                
            user_id = _ANONYM
            pasw    = '?'
            rmbr    = False

            self.user = User(self.journal)
            self.user.authenticate(user_id, pasw)
            login_user(self.user, remember=rmbr)

            self.journal.M(f"{self.name}.resp: Continue as Guest User")
            self.journal.O()
            return redirect(self.urlFor('pgHomepage'))

        #----------------------------------------------------------------------
        # Logout
        #----------------------------------------------------------------------
        if self.form.btnLogout.data:
                
            logout_user()
            
            self.journal.M(f"{self.name}.resp: Logout")
            self.journal.O()
            return redirect(self.urlFor('pgLogin'))

        #----------------------------------------------------------------------
        # User uz je autentifikovany
        #------------------------------------------------------------------
        if False and self.user.is_authenticated:
               
            self.journal.M(f"{self.name}.respPost: '{self.user.user_id}' is autheticated already")
            self.journal.O()
            return redirect(self.urlFor('pgHomepage'))

        #----------------------------------------------------------------------
        # Vyhodnotim formular
        #----------------------------------------------------------------------
        if self.form.validate_on_submit():
            
            #------------------------------------------------------------------
            # Vytvornie usera podla udajov z formulara
            #------------------------------------------------------------------
            user_id = self.form.username.data
            pasw    = self.form.password.data
            rmbr    = self.form.remember.data
            
            self.user = User(self.journal)

            #------------------------------------------------------------------
            # Autentifikacia usera podla udajov z formulara sa nepodarila
            #------------------------------------------------------------------
            if not self.user.authenticate(user_id, pasw):
                
                logout_user()
                flash('Invalid username or password')
                self.journal.M(f"{self.name}.respPost: Authentication failed")
                self.journal.O()
                return redirect(self.urlFor('pgLogin'))

            #------------------------------------------------------------------
            # User je autentifikovany, zapisem do session
            #------------------------------------------------------------------
            login_user(self.user, remember=rmbr)

            self.journal.M(f"{self.name}.resp: User logged in")
            self.journal.O()
            return redirect(self.urlFor('pgHomepage'))
 
        #----------------------------------------------------------------------
        # Default redirect
        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.resp: Default response")
        self.journal.O()
        return redirect(self.urlFor('pgLogin'))
   
    #==========================================================================
    # Form methods
    #--------------------------------------------------------------------------
    def formFromPost(self):
        "This method cretes form based on POST data"
        
        self.journal.I(f"{self.name}.formFromPost: {self.POST}")
        self.journal.M(f"{self.name}.formFromPost   : formType='LoginForm'", True)
        
        #----------------------------------------------------------------------
        # Vytvorenie Login formulara z post data
        #----------------------------------------------------------------------
        try   : self.form = LoginForm(formdata=self.POST, formType="LoginForm")
        except: self.journal.M(f"{self.name}.formFromPost   : Ouside context, form was not created", True)

        #----------------------------------------------------------------------
        self.journal.O()

    #--------------------------------------------------------------------------
    def formDataFromDb(self):
        "This method loads tuple (dbItem, dbData) from DMS/Database"
        
        self.journal.M(f"{self.name}.formDataFromDb : No data in DB for login", True)

        self.dbData    = []                  # Data content from DMS/Formular
        self.dbItem    = []                  # Item content from DMS

        #----------------------------------------------------------------------
        return (self.dbData, self.dbItem)
    
    #==========================================================================
    # HTML methods
    #--------------------------------------------------------------------------
#!!!!
    def htmlHead(self):
        """"This method should be overrided and return html code
            for the head space of this window"""
        
        toRet = ''
        
        #----------------------------------------------------------------------
        # Vytvorenie hlavicky objektu podla class
        #----------------------------------------------------------------------
        title  = 'SIQO Login'
        toRet += self.itemRender({self.lang:title})

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlBack(self):
        """"This method should be overrided and return html code
            for the back space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Render the object formular
        #----------------------------------------------------------------------

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlFront(self):
        """"This method should be overrided and return html code
            for the front space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Vytvorenie Front/end objektu podla class
        #----------------------------------------------------------------------
        toRet += str(self.form.username.label())
        toRet += str(self.form.username(class_="ObjectInputString", size=35))
        toRet += self.breakLine()
        
        if len(self.form.username.errors)>0:
            
            for error in self.form.username.errors:
                
                toRet += f'<span style="color: red;">{error}</span>'
            
        #----------------------------------------------------------------------
        toRet += str(self.form.password.label())
        toRet += str(self.form.password(class_="ObjectInputString", size=35))
        toRet += self.breakLine()

        if len(self.form.password.errors)>0:
            
            for error in self.password.username.errors:
                
                toRet += f'<span style="color: red;">{error}</span>'

        #----------------------------------------------------------------------
        toRet += str(self.form.remember())
        toRet += str(self.form.remember.label(style="width:9em;"))

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlControll(self):
        """"This method should be overrided and return html code
            for the controll space of this window"""

        toRet = ''

        toRet += str(self.form.btnLogin (class_="ObjectControlBtn"))
        toRet += str(self.form.btnGuest (class_="ObjectControlBtn"))
        toRet += str(self.form.btnLogout(class_="ObjectControlBtn"))

        #----------------------------------------------------------------------
        return toRet
    
#==============================================================================
print(f"w_login {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
