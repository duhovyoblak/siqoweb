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

import siqolib.general         as gen

import dms             as dms

from   database        import Database
from   config          import Config
from   user            import User
from   p_structure     import Structure
from   forms           import FormLogin


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
# Page
#------------------------------------------------------------------------------
class Page(Structure):
    
    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadContent(self):
        
        self.journal.I(f"{self.name}.loadContent:")

        self.journal.O()
        return {'content':[{'key':'val'}]}

    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost:")
        
        #----------------------------------------------------------------------
        # Ak je POST, najprv vyhodnotim formular formLogin
        #----------------------------------------------------------------------
        if self.formLogin.validate_on_submit():
            
            self.journal.M(f"{self.name}.resp: User logged in")
            self.journal.O()
            return redirect(url_for('homepage'))
 
        #----------------------------------------------------------------------
        # Nie je POST
        #----------------------------------------------------------------------
        self.journal.O()
        return None

    #--------------------------------------------------------------------------

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

    page = Page(journal, env, 'Homepage', 700)
    

#==============================================================================
print(f"Page {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
