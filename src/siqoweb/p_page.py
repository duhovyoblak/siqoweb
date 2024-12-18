#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask              import url_for, get_flashed_messages, flash, render_template, make_response
from   flask              import request, session, abort, redirect
from   flask_login        import login_user, logout_user, current_user

from   markupsafe         import escape
from   wtforms.validators import ValidationError

import jinja2             as j2
from   jinja2             import Environment, FileSystemLoader, PackageLoader, select_autoescape

import siqolib.general    as gen

from   database           import Database
from   config             import Config
from   app_user           import User
from   p_structure        import Structure


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.01'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Page
#------------------------------------------------------------------------------
class Page(Structure):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, env, classId, target, height, template="1 structure.html"):
        "Call constructor of Page and initialise it"
        
        journal.I(f"Page({classId}).init:")
        
        #----------------------------------------------------------------------
        # Identifikacia usera
        #----------------------------------------------------------------------
        user = current_user
        
        if user is not None and str(user)[:5]=='User>': 
            
            self.userId   = user.user_id
            self.userName = user.userName()
            self.lang     = user.lang_id
            
        else: 
            self.userId   = 'Anonymous'
            self.userName = 'Guest User'
            self.lang     = 'SK'

        #----------------------------------------------------------------------
        # Konstruktor DataStructure,
        #----------------------------------------------------------------------
        super().__init__(journal, env, self.userId, classId, height, template)
        
        self.name   = f"Page({self.name})"
        self.target = target                  # Nazov route metody pre page

        #----------------------------------------------------------------------
        # Aktualny user a jazyk
        #----------------------------------------------------------------------
        journal.M(f"{self.name}).init: user = '{self.userName}'")
        journal.M(f"{self.name}).init: lang = '{self.lang}'")

        self.journal.O()
       
    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadContent(self):
        "This method should return page specific content like forms, objects etc."
        
        self.journal.I(f"{self.classId}.loadContent:")
        
        self.journal.O()
        return {}

    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def resp(self):
     
        self.journal.I(f"{self.name}.resp:")
        
        #----------------------------------------------------------------------
        # Vypisem si request data
        #----------------------------------------------------------------------
#        self.journal.M(f"{self.name}.resp: user_agent       {request.user_agent}", True)
        self.journal.M(f"{self.name}.resp: remote_addr      {request.remote_addr}", True)
        self.journal.M(f"{self.name}.resp: is_secure        {request.is_secure}", True)
#        self.journal.M(f"{self.name}.resp: form             {request.form}", True)
        self.journal.M(f"{self.name}.resp: data             {request.data}", True)
        self.journal.M(f"{self.name}.resp: args             {request.args}", True)
        self.journal.M(f"{self.name}.resp: access_route     {request.access_route}", True)

        self.journal.M(f"{self.name}.resp: headers.Referer  {request.headers.get('Referer')}", True)
#        self.journal.M(f"{self.name}.resp: headers.Cookie   {request.headers.get('Cookie' )}", True)


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
            
            try: resp = self.respPost()
            except ValidationError as err: print(str(err))
            
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

    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost: Default None post response")
        
        
        
        
        self.journal.O()
        return None

    #--------------------------------------------------------------------------
    def respGet(self):
     
        self.journal.I(f"{self.name}.respGet: Default html get response from template='{self.template}'")
        
        #----------------------------------------------------------------------
        # Doplnenie dynamickeho contextu idx
        #----------------------------------------------------------------------
        self.idContext = self.loadContent()
        self.addContext(self.idContext)

        #----------------------------------------------------------------------
        # Vytvorenie template
        #----------------------------------------------------------------------
        template = self.env.get_template(self.template)
        self.journal.M(f"{self.name}.respGet: template loaded")

        #----------------------------------------------------------------------
        # Vygenerujem html response
        #----------------------------------------------------------------------
        resp = make_response(template.render(**self.context), 200)
        
        # V pripade potreby vies doplnit headers o custom data
        # resp.headers['X-Something'] = 'A value'
        
        self.journal.O()
        return resp

    #--------------------------------------------------------------------------
    # Default and emergency redirects
    #--------------------------------------------------------------------------
    def toLogin(self):
     
        return redirect(url_for('pgLogin'))

    #--------------------------------------------------------------------------
    def toHomepage(self):
     
        return redirect(url_for('pgHomepage'))

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal              import SiqoJournal
    journal = SiqoJournal('test-base', debug=5)
    
    env = Environment(
    
     autoescape = select_autoescape()
    ,loader     = FileSystemLoader(['templates'])
    )

    page = Page(journal, env, 'Homepage', 700)
    

#==============================================================================
print(f"Page {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
