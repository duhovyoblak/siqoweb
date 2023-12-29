#==============================================================================
#  SIQO Homepage: homepage
#------------------------------------------------------------------------------
import os

from   flask                    import url_for, render_template, make_response
from   flask                    import request, session, abort, redirect
from   markupsafe               import escape

import jinja2 as j2
from   jinja2          import Environment, PackageLoader, select_autoescape

import siqo_general  as gen
import web_lib       as wl

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_IS_TEST  = True if os.environ['wsiqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = None

env = Environment(
    
    autoescape = select_autoescape()
#     loader     = PackageLoader("SIQO")
)


#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# 
#------------------------------------------------------------------------------
def index():
    
    resp = make_response(render_template('index.html', is_test=_IS_TEST), 200)
    resp.headers['X-Something'] = 'A value'

    return resp

#------------------------------------------------------------------------------
def homepage():
    
    selpage = gen.loadJson(journal, fileName='../DMS/homepage.json')
    
    context = wl.selpageContext(selpage)
    
    for k, v in context.items():
        
        print()
        print(k, '...:', v)
    
    resp = make_response(render_template('page.html', **context), 200)
    resp.headers['X-Something'] = 'A value'

    return resp

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"homepage {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
