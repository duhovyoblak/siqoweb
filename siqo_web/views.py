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
from   siqo_web.page      import Page

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

    page = Page(journal, 'homePage', env, "_page.html", 'homepage.json', height=770)

    resp = page.resp()

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
