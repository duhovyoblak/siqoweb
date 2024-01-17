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
from siqo_web.pageBase    import PageBase


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
class Page(PageBase):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, name, env, template, pageDms, height):
        "Call constructor of Page and initialise template and dms content"
        
        #----------------------------------------------------------------------
        # Initialise PageBase
        #----------------------------------------------------------------------
        super().__init__(journal, name, env, template, pageDms, height)
        self.name = name
        
        #----------------------------------------------------------------------
        self.journal.I(f"{self.name}.init:")
        
        #----------------------------------------------------------------------
        # Doplnenie Page contextu
        #----------------------------------------------------------------------
        self.pageContext(self.data)
    
        self.journal.O()
        
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def pageContext(self, data):
        "Creates context from json-encoded selector page"
    
        self.journal.I(f"{self.name}.context:")

        #----------------------------------------------------------------------
        # Creating selectors and panels
        #----------------------------------------------------------------------
        selectors = []
        panels    = []
    
        i = 0
        for sel in data["sels"]:
        
            selectors.append( { "id"     : f"SSB_{sel['id']}"
                           ,"value"  : sel['id']
                           ,"onclick": f"ShowStage('{sel['id']}')"
                           ,"title"  : sel["title"]
                          } )
        
            if i==0: style = "display:block"
            else   : style = "display:none"
        
            panels.append( { "id"     : f"SP_{sel['id']}"
                         ,"style" : style
                         ,"header": sel['header']
                         ,"item"  : self.renderItem(sel['item'])
                       }) 
        
            i += 1
    
        #----------------------------------------------------------------------
        self.context['selectors'] = selectors
        self.context['panels'   ] = panels

        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.context = {self.context}")
        self.journal.O()

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
print(f"Page {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
