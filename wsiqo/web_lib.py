#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   flask                    import url_for, render_template, make_response
from   flask                    import request, session, abort, redirect
from   markupsafe               import escape

import jinja2 as j2
from jinja2          import Environment, PackageLoader, select_autoescape


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_IS_TEST  = True if os.environ['wsiqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------


#==============================================================================
# page's tools
#------------------------------------------------------------------------------
def selpageContext(selpage):
    "Creates context from json-encoded selector page"
    
    toRet = {}
    
    toRet["title"        ]= selpage["title"        ]
    toRet["head_title"   ]= selpage["head_title"   ]
    toRet["head_subtitle"]= selpage["head_subtitle"]
    toRet["head_comment" ]= selpage["head_comment" ]
    toRet["user"         ]= "guest user"
    
    #--------------------------------------------------------------------------
    # Creating selectors and panels
    #--------------------------------------------------------------------------
    selectors = []
    panels    = []
    
    i = 0
    for sel in selpage["sels"]:
        
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
                         ,"item"  : renderItem(sel['item'])
                       }) 
        
        i += 1
    
    #--------------------------------------------------------------------------
    toRet['selectors'] = selectors
    toRet['panels'   ] = panels

    #--------------------------------------------------------------------------
    return toRet

#==============================================================================
# rendering functions
#------------------------------------------------------------------------------
def renderItem(item):
    "Returns HTML for json-encoded item"
    
    toRet = ""
    
    toRet = item
    
    return toRet


#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"web_lib {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
