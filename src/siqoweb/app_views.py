#==============================================================================
#  SIQO Homepage: homepage
#------------------------------------------------------------------------------
import os

from   flask              import make_response
from   flask              import request, session, abort, redirect
from   markupsafe         import escape

from   jinja2             import Environment, FileSystemLoader, select_autoescape

from   p__page            import Page
from   p_login            import PageLogin
from   p_forum            import PageForum

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.04'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = None

env = Environment(
    
     autoescape = select_autoescape()
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
def pgLogin():
    
    journal.I('app_views.pgLogin()')

    page = PageLogin(journal, env, 'PagManLogin', height=670, template="3 login.html")
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgEmpty(classId, height=670):
    
    journal.I('app_views.pgEmpty()')

    page = Page(journal, env, classId=classId, height=height, template="3 empty.html")
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgStaged(classId, height=670):
    
    journal.I('app_views.pgHomepage()')

    page = Page(journal, env, classId=classId, height=height, template="3 staged.html")
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgForum(classId, target, idx=0, height=670):
    
    journal.I('app_views.pgForum()')

    page = PageForum(journal, env, classId=classId, target=target, idx=idx, height=height, template="3 empty.html")
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
