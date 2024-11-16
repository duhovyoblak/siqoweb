#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask              import url_for, get_flashed_messages, flash, render_template, make_response
from   flask              import request, session, abort, redirect
from   flask_login        import login_user, logout_user, current_user
from   markupsafe         import escape

import jinja2             as j2
from   jinja2             import Environment, FileSystemLoader, PackageLoader, select_autoescape

import siqolib.general    as gen
from   config             import Config
from   app_user           import User, _ANONYM
from   p_structure        import Structure
from   f_formLogin        import FormLogin


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.03'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Login
#------------------------------------------------------------------------------
class PageLogin(Structure):
    
    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadContent(self):
        "This method should return page specific content like forms, objects etc."
        
        self.journal.I(f"{self.name}.loadContent:")

        #----------------------------------------------------------------------
        # Doplnenie formLogin
        #----------------------------------------------------------------------
        self.formLogin = FormLogin()

        self.journal.O()
        return {"formLogin":self.formLogin}

    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost:")
        
        #----------------------------------------------------------------------
        # Continue as Guest User
        #----------------------------------------------------------------------
        if self.formLogin.btnGuest.data:
                
                user_id = _ANONYM
                pasw    = '?'
                rmbr    = False

                self.user = User(self.journal)
                self.user.authenticate(user_id, pasw)
                login_user(self.user, remember=rmbr)

                self.journal.M(f"{self.name}.resp: Continue as Guest User")
                self.journal.O()
                return redirect(url_for('pgHomepage'))

        #----------------------------------------------------------------------
        # Logout
        #----------------------------------------------------------------------
        if self.formLogin.btnLogout.data:
                
                logout_user()
            
                self.journal.M(f"{self.name}.resp: Logout")
                self.journal.O()
                return redirect(url_for('pgLogin'))

        #----------------------------------------------------------------------
        # User uz je autentifikovany
        #------------------------------------------------------------------
        if False and self.user.is_authenticated:
               
            self.journal.M(f"{self.name}.respPost: '{self.user.user_id}' is autheticated already")
            self.journal.O()
            return redirect(url_for('pgHomepage'))

        #----------------------------------------------------------------------
        # Vyhodnotim formular formLogin
        #----------------------------------------------------------------------
        if self.formLogin.validate_on_submit():
            
            #------------------------------------------------------------------
            # Vytvornie usera podla udajov z formulara
            #------------------------------------------------------------------
            user_id = self.formLogin.username.data
            pasw    = self.formLogin.password.data
            rmbr    = self.formLogin.remember.data
            
            self.user = User(self.journal)

            #------------------------------------------------------------------
            # Autentifikacia usera podla udajov z formulara sa nepodarila
            #------------------------------------------------------------------
            if not self.user.authenticate(user_id, pasw):
                
                logout_user()
                flash('Invalid username or password')
                self.journal.M(f"{self.name}.respPost: Authentication failed")
                self.journal.O()
                return redirect(url_for('pgLogin'))

            #------------------------------------------------------------------
            # User je autentifikovany, zapisem do session
            #------------------------------------------------------------------
            login_user(self.user, remember=rmbr)

            self.journal.M(f"{self.name}.resp: User logged in")
            self.journal.O()
            return redirect(url_for('pgHomepage'))
 
        #----------------------------------------------------------------------
        # Default redirect
        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.resp: Default response")
        self.journal.O()
        return redirect(url_for('pgLogin'))

    #--------------------------------------------------------------------------

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"Login {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
