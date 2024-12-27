#==============================================================================
#                                                     (c) SIQO 24
# Class Login for SIQO Flask application
#
#------------------------------------------------------------------------------
import os
import re
import traceback

from   datetime                 import date
from   flask                    import request, url_for

from   o__object                import Object
from   w_Login_f                import LoginForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.10'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
#journal = None
#db      = None

#==============================================================================
# Class Login
#------------------------------------------------------------------------------
class Login(Object):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dms, userId, lang, item, idx=0, height=20, width=20):

        journal.I(f"Login.__init__: for {userId}")

        #----------------------------------------------------------------------
        # Inicializacia Window
        #----------------------------------------------------------------------
        super().__init__(journal, dms, userId, lang, item, idx, height=height, width=width) # classId=OBJECT_ID v pagman db

        self.name      = f"Login({self.name})"
        self.formId    = f"LoginForm_{self.idx}"  # Id of the formular
       
        #----------------------------------------------------------------------
        # Nacitanie formulara s POST udajmi
        #----------------------------------------------------------------------
        self.loadForm()

        self.journal.O()

    #==========================================================================
    # Form methods
    #--------------------------------------------------------------------------
    def loadForm(self):
        "This method should return class specific content like forms, objects etc."
        
        self.journal.I(f"{self.name}.loadForm:")
        
        #----------------------------------------------------------------------
        # Ziskanie post data
        #----------------------------------------------------------------------
        self.formPost  = request.form

        #----------------------------------------------------------------------
        # Vytvorenie Login formulara z post data
        #----------------------------------------------------------------------
        self.form = LoginForm(formdata=self.formPost)

        self.journal.O()

    #==========================================================================
    # DB Persistency methods
    #--------------------------------------------------------------------------
    def dbLoad(self):
        """"This method should be overrided and load tuple (dbItem, dbData) 
            from DMS/Database"""
        
        self.dbData    = []                  # Data content from DMS/Formular
        self.dbItem    = []                  # Item content from DMS

        #----------------------------------------------------------------------
        return (self.dbData, self.dbItem)
    
    #--------------------------------------------------------------------------
    def dbSave(self):
        """"This method should be overrided and save dbData 
            into DMS/Database"""
        
       
        #----------------------------------------------------------------------
        print('dbData > ', self.dbData)
    
    #==========================================================================
    # HTML methods
    #--------------------------------------------------------------------------
#!!!!
    #--------------------------------------------------------------------------
    def htmlHead(self):
        """"This method should be overrided and return html code
            for the head space of this window"""
        
        toRet = ''
        
        #----------------------------------------------------------------------
        # Vytvorenie hlavicky objektu podla class
        #----------------------------------------------------------------------
        title  = 'SIQO Login'
        toRet += self.itemRender(title, self.lang)

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlBack(self, objClass, item, dbItem, dbData, lang):
        """"This method should be overrided and return html code
            for the back space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Render the object formular
        #----------------------------------------------------------------------
        method = 'POST'
        action = ""  #url_for(self.target)
        toRet += self.formStart({"method":method, "action":action, "enctype":"multipart/form-data"})
            





        toRet += str(self.form.hidden_tag())
        
        self.formStop()

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
        toRet += str(self.formLogin.username.label())
        toRet += str(self.formLogin.username( class_="ObjectInputString", value="Login", size=35))
        toRet += self.breakLine()
        
        if len(self.formLogin.username.errors)>0:
            
            for error in self.formLogin.username.errors:
                
                toRet += f'<span style="color: red;">{error}</span>'
            
        #----------------------------------------------------------------------
        toRet += str(self.formLogin.password.label())
        toRet += str(self.formLogin.password(size=35))
        toRet += self.breakLine()

        if len(self.formLogin.password.errors)>0:
            
            for error in self.password.username.errors:
                
                toRet += f'<span style="color: red;">{error}</span>'

        #----------------------------------------------------------------------
        toRet += str(self.formLogin.remember())
        toRet += str(self.formLogin.remember.label())

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlControll(self):
        """"This method should be overrided and return html code
            for the controll space of this window"""

        toRet = ''

        toRet += str(self.form.formLogin.btnLogin (class_="ObjectControlBtn"))
        toRet += str(self.form.formLogin.btnGuest (class_="ObjectControlBtn"))
        toRet += str(self.form.formLogin.btnLogout(class_="ObjectControlBtn"))

        #----------------------------------------------------------------------
        return toRet
    
#==============================================================================
print(f"w_login {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
