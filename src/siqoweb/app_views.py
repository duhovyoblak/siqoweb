#==============================================================================
#  SIQO Homepage: homepage
#------------------------------------------------------------------------------
import os

from   flask              import make_response
from   flask              import request, session, abort, redirect
from   markupsafe         import escape

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

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# System's app_views 
#------------------------------------------------------------------------------
def pgLogin():
    
    journal.I('app_views.pgLogin()')

    page = PageLogin(journal, title='Login', classId='PagManLogin', height=670)
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgEmpty(title, classId, height=670):
    
    journal.I('app_views.pgEmpty()')

    page = Page(journal, title=title,classId=classId, height=height)
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgStaged(title, classId, height=670):
    
    journal.I('app_views.pgHomepage()')

    page = Page(journal, title=title, classId=classId, height=height)
    resp = page.resp()

    journal.O()
    return resp

#------------------------------------------------------------------------------
def pgForum(title, classId, target, idx=0, height=670):
    
    journal.I('app_views.pgForum()')

    page = PageForum(journal, title=title, classId=classId, target=target, idx=idx, height=height)
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
