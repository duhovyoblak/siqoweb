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
from   siqo_web.user            import User, _ANONYM
from   siqo_web.p_structure     import Structure
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
# Login
#------------------------------------------------------------------------------
class Login(Structure):
    
    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadContent(self):
        
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
        if self.formLogin.conti.data:
                
                user_id = _ANONYM
                pasw    = '?'
                rmbr    = False

                self.user = User(self.journal)
                self.user.authenticate(user_id, pasw)
                login_user(self.user, remember=rmbr)

                self.journal.M(f"{self.name}.resp: Continue as Guest User")
                self.journal.O()
                return redirect(url_for('homepage'))

        #----------------------------------------------------------------------
        # Logout
        #----------------------------------------------------------------------
        if self.formLogin.logout.data:
                
                logout_user()
            
                self.journal.M(f"{self.name}.resp: Logout")
                self.journal.O()
                return redirect(url_for('homepage'))

        #----------------------------------------------------------------------
        # User uz je autentifikovany
        #------------------------------------------------------------------
        if False and self.user.is_authenticated:
               
            self.journal.M(f"{self.name}.respPost: '{self.user.user_id}' is autheticated already")
            self.journal.O()
            return redirect(url_for('homepage'))

        #----------------------------------------------------------------------
        # Vyhodnotim formular formLogin
        #----------------------------------------------------------------------
        if self.formLogin.validate_on_submit():
            
            #------------------------------------------------------------------
            # Autentifikacia usera podla udajov z formulara
            #------------------------------------------------------------------
            user_id = self.formLogin.username.data
            pasw    = self.formLogin.password.data
            rmbr    = self.formLogin.remember.data
            
            self.user = User(self.journal)

            if not self.user.authenticate(user_id, pasw):
                
                logout_user()
                flash('Invalid username or password')
                self.journal.M(f"{self.name}.respPost: Authentication failed")
                self.journal.O()
                return redirect(url_for('login'))

            #------------------------------------------------------------------
            # User je autentifikovany, zapisem do session
            #------------------------------------------------------------------
            login_user(self.user, remember=rmbr)

            self.journal.M(f"{self.name}.resp: User logged in")
            self.journal.O()
            return redirect(url_for('homepage'))
 
        #----------------------------------------------------------------------
        # Default redirect
        #----------------------------------------------------------------------
        self.journal.O()
        return None

    #--------------------------------------------------------------------------

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"Login {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
