#==============================================================================
#  SIQO Homepage: web routes operations
#------------------------------------------------------------------------------
import os

from   flask                    import Flask, url_for, render_template, make_response
from   flask                    import request, session, abort, redirect
from   markupsafe               import escape

from   siqo_web.config          import Config
from   siqo_web.forms           import FormLogin
import siqo_web.views           as views

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_CWD      = os.getcwd()
_IS_TEST  = True if os.environ['wsiqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = None
_app    = None

#==============================================================================
# package's tools
#------------------------------------------------------------------------------
def getApp():

    print("getApp():")

    global _app

    #--------------------------------------------------------------------------
    # Ak Flask aplikacia neexistuje, vytvorim ju
    #--------------------------------------------------------------------------
    if _app is None:
    
        print("getApp(): Creating application...")
        
        _app = Flask(__name__, static_url_path=None, static_folder='static', 
                     template_folder='templates', instance_path=None, 
                     instance_relative_config=False, root_path=None)
    
        _app.config.from_object(Config)
    
        print("getApp(): Flask app {_app} was created at {id(_app)} in {__name__}")

    #--------------------------------------------------------------------------
    return _app

#------------------------------------------------------------------------------
app = getApp()

#==============================================================================
# package's tools
#------------------------------------------------------------------------------
def shutdownServer():

    journal.I("shutdownServer():")

    from win32api import GenerateConsoleCtrlEvent
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)

    journal.O()
    
#------------------------------------------------------------------------------
#@app.errorhandler(404)
#def page_not_found(error):
    
#    resp = make_response(render_template('error.html'), 404)
#    resp.headers['X-Something'] = 'A value'

#    return resp

#Note the 404 after the render_template() call. This tells Flask that the status code of that page should be 404 which means not found. By default 200 is assumed which translates to: all went well.


#@app.before_request
#==============================================================================
# PATHs operation
#------------------------------------------------------------------------------
@app.get("/")
@app.get("/index")
def index():

    journal.M("index():")
    return views.index()

#------------------------------------------------------------------------------
@app.get('/shutdown')
def shutdown():
    
    journal.I("shutdown():")

    if _IS_TEST: 
        shutdownServer()
        
    else: 
        journal.O()
        abort(404)

    journal.O()
    return 'Server was shut down...'

#------------------------------------------------------------------------------
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():

    journal.M("homepage():")
    return views.homepage()
    
#------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    
    journal.M("logout():")
    
    # remove the username from the session if it's there
    session.pop('username', None)

    return redirect(url_for('index'))

#------------------------------------------------------------------------------
@app.get('/user/<username>')
def profile(username):

    journal.M(f"profile(): username='{username}'")

    # show the user profile for that user
    return f"User {escape(username)}"

#------------------------------------------------------------------------------
@app.route('/post/<int:postId>')
def show_post(postId):

    journal.M(f"show_post(): postId='{postId}'")

    # show the post with the given id, the id is an integer
    return f"Post {postId}"

#------------------------------------------------------------------------------
@app.route('/path/<path:subpath>')
def show_subpath(subpath):

    journal.M(f"show_subpath(): subpath='{subpath}'")

    # show the subpath after /path/
    return f"Subpath {escape(subpath)}"

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
with app.test_request_context():
    print(url_for('index'))
    print(url_for('profile', username='John Doe'))
    print(url_for('static', filename='css/base_page.css'))
    
#==============================================================================
print(f"routes {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
