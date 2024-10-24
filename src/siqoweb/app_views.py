#==============================================================================
#  SIQO Homepage: homepage
#------------------------------------------------------------------------------
import os

from   flask              import url_for, render_template, make_response
from   flask              import request, session, abort, redirect
from   markupsafe         import escape

import jinja2 as j2
from   jinja2             import Environment, FileSystemLoader, PackageLoader, select_autoescape

import siqolib.general   as gen

from   p_structure      import Structure
from   p_login          import Login
from   p_page           import Page
from   p_forum          import Forum

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = None

env = Environment(
    
     autoescape = select_autoescape()
#    ,loader     = PackageLoader(package_name="siqoweb", package_path="templates")
    ,loader     = FileSystemLoader(['templates'])
)

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# System's app_views 
#------------------------------------------------------------------------------
def index():
    
    journal.I('app_views.index()')
    
    template = env.get_template("index.html")
    
    resp = make_response(template.render(is_test=_IS_TEST), 200)
    resp.headers['X-Something'] = 'A value'

    journal.O()
    return resp

#------------------------------------------------------------------------------
def structure():
    
    journal.I('app_views.structure()')

    page = Structure(journal, env, 'Login', height=670)
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def login():
    
    journal.I('app_views.login()')

    page = Login(journal, env, 'Login', height=670, template="3 login.html")
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def homepage():
    
    journal.I('app_views.homepage()')

    page = Page(journal, env, 'Homepage', height=670, template="3 staged.html")
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgdocument():
    
    journal.I('app_views.pgdocument()')

    page = Page(journal, env, 'PagManDocument', height=670, template="3 empty.html")
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgresource():
    
    journal.I('app_views.pgresource()')

    page = Page(journal, env, 'Resource', height=670, template="3 empty.html")
    resp = page.resp()

    journal.O()
    return resp

#==============================================================================
# Content's app_views 
#------------------------------------------------------------------------------
def oralhistory(idx):
    
    journal.I(f'app_views.oralhistory({idx})')

    page = Forum(journal, env, 'OHISTORY', idx=idx, height=670)
    resp = page.resp()

    journal.O()
    return resp

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"app_views {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
