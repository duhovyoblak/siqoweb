#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask               import url_for, get_flashed_messages, flash, render_template, make_response
from   flask               import request, session, abort, redirect
from   flask_login         import login_user, logout_user, current_user
from   markupsafe          import escape

import jinja2              as j2
from   jinja2              import Environment, FileSystemLoader, select_autoescape

import siqolib.general     as gen
from   config              import Config
from   database            import Database
from   app_user            import User
from   app_dms             import DMS
from   p_page              import Page
from   f_formForum         import FormForum

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.03'

_DAY_CHANGES   = 32       # Pocet dni, pocas ktorych sa item povazuje za cerstvo zmeneny
_TITLE_MAX     = 36       # Maximalny pocet zobrazenych znakov TITLE v selectore

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Forum
#------------------------------------------------------------------------------
class PageForum(Page):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, env, classId, target, idx=0, height=700, template="3 forum.html"):
        "Call constructor of Forum and initialise it"
        
        journal.I(f"PageForum.init: Class '{classId}' for target {target}?idx={idx}")
        
        #----------------------------------------------------------------------
        # Forum premenne
        #----------------------------------------------------------------------
        self.target      = target        # Nazov route metody pre zvolene forum
        self.idx         = idx           # Cislo itemu, default = 0 pre root
        self.forumItem   = None          # Forum item nacitany z DB vo forme dict
        self.form        = FormForum()   # Formular pre Forum 

        #----------------------------------------------------------------------
        # Konstruktor Structure
        #----------------------------------------------------------------------
        super().__init__(journal, env, classId=classId, height=height, template=template)
        
        #----------------------------------------------------------------------
        # Doplnenie dynamickych odkazov pre html_renderer
        #----------------------------------------------------------------------
        self.html.dynIdx  = self.idx
        self.html.dynForms.append(self.form)


        self.journal.O()

    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost:")
        
        #print(self.form.data)
        
        #----------------------------------------------------------------------
        # Ak je POST, najprv vyhodnotim formular formLogin
        #----------------------------------------------------------------------
        if self.form.validate():
            
            self.journal.M(f"{self.name}.respPost: form validated", True)
            self.journal.O()
            return redirect(url_for('pgHomepage'))
 
        #----------------------------------------------------------------------
        # Nie je POST
        #----------------------------------------------------------------------
        print()
        print(self.form.errors)
        self.journal.M(f"{self.name}.respPost: form NOT validated", True)
        self.journal.O()
        return None

    #==========================================================================
    # Private methods

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal                 import SiqoJournal
    journal = SiqoJournal('test-base', debug=6)
    
    env = Environment(
     autoescape = select_autoescape()
    ,loader     = FileSystemLoader(['templates'])
    )

    page = PageForum(journal, env, classId='OHISTORY', target='pgOhistory', idx=68, height=700)
    rec  = page.context

#==============================================================================
print(f"Forum {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
