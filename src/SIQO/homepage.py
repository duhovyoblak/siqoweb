#==============================================================================
#  SIQO Homepage: homepage
#------------------------------------------------------------------------------
import os

from   flask                    import Flask, url_for, render_template, make_response
from   flask                    import request, session, abort, redirect
from   markupsafe               import escape

import jinja2 as j2
from jinja2          import Environment, PackageLoader, select_autoescape


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_IS_TEST  = True if os.environ['siqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
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
    
    context = {"title": "SIQO Homepage"
              ,"width": 1000
              }
    
    resp = make_response(render_template('base.html', **context), 200)
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
