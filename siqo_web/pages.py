#==============================================================================
#  SIQO Homepage: homepage
#------------------------------------------------------------------------------
import os

from   flask              import url_for, render_template, make_response
from   flask              import request, session, abort, redirect
from   markupsafe         import escape

import jinja2 as j2
from   jinja2             import Environment, FileSystemLoader, PackageLoader, select_autoescape

import siqo_lib.general   as gen
import siqo_web.dms       as dms
import siqo_web.web_lib   as wl

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
    ,loader     = PackageLoader(package_name="siqo_web", package_path="templates")
)

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# 
#------------------------------------------------------------------------------
def index():
    
    journal.I('index()')
    
    template = env.get_template("index.html")
    
    resp = make_response(template.render(is_test=_IS_TEST), 200)
    resp.headers['X-Something'] = 'A value'

    journal.O()
    return resp

#------------------------------------------------------------------------------
def homepage():
    
    journal.I('homepage()')
    
    selpage = dms.loadJson('homepage.json')
    
    context = wl.selpageContext(selpage)
    context["url_for"] = url_for
 
#    journal.M( gen.dictString(context) )
     
    template = env.get_template("page.html")
    resp = make_response(template.render(**context), 200)
    resp.headers['X-Something'] = 'A value'

    journal.O()
    return resp

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"pages {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
