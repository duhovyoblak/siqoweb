#==============================================================================
#  SIQO Homepage: app_routes methods
#------------------------------------------------------------------------------
from   flask                    import Flask, url_for, make_response
from   flask                    import request, session, abort, redirect
from   flask                    import get_flashed_messages, flash
from   flask_login              import LoginManager, login_required, login_user, current_user
from   markupsafe               import escape

from   siqoweb.config           import Config
from   siqoweb.app_user         import User
import siqoweb.app_views        as app_views

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER        = '1.08'
_LOGIN_VIEW = 'pgLogin'


#==============================================================================
# package's variables
#------------------------------------------------------------------------------
_app    = None
_login  = None
journal = None

#==============================================================================
# package's tools
#------------------------------------------------------------------------------
def getApp():

    print("getApp():")

    global _app, _login

    #--------------------------------------------------------------------------
    # Ak Flask aplikacia neexistuje, vytvorim ju
    #--------------------------------------------------------------------------
    if _app is None:
    
        print("getApp(): Creating application...")
        
        _app = Flask(__name__, static_url_path=None, static_folder='static', 
                     template_folder='templates', instance_path=None, 
                     instance_relative_config=False, root_path=None)
    
        _app.config.from_object(Config)
        print(f"getApp(): Flask app {_app} was created at {id(_app)} in {__name__}")
        
        _login = LoginManager(_app)
        _login.login_view = _LOGIN_VIEW
        print(f"getApp(): LoginManager was created at {id(_login)}")

    #--------------------------------------------------------------------------
    return (_app, _login)

#------------------------------------------------------------------------------
app, loginManager = getApp()

#==============================================================================
# package's tools
#------------------------------------------------------------------------------
def shutdownServer():

    journal.I("shutdownServer():")

    func = request.environ.get('werkzeug.server.shutdown')
    
    if func is None: raise RuntimeError('Not running with the Werkzeug Server')
    else           : func()
    
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
# Sytem PATHs operation
#------------------------------------------------------------------------------
@app.get("/")
@app.get("/index")
def index():

    journal.M("index():")
    
    resp = app.send_static_file('html/index.html')
    resp.headers['X-Something'] = 'A value'

    return resp

#------------------------------------------------------------------------------
@app.get('/shutdown')
def shutdown():
    
    journal.I("shutdown():")

    if 1==1: 
        shutdownServer()
        
    else: 
        journal.O()
        abort(404)

    journal.O()
    return 'Server was shut down...'

#==============================================================================
# LOGIN operation
#------------------------------------------------------------------------------
@loginManager.user_loader
def load_user(user_id='Anonymous'):
    """This callback is used to reload the user object from the user ID stored 
    in the session. It should take the str ID of a user, and return the 
    corresponding user object. It should return None (not raise an exception) if
    the ID is not valid."""
    
    journal.I(f"load_user(): '{user_id}'")
    
    user  = User(journal)
    toRet = user.load(user_id)
    
    if toRet is None: journal.M(f"load_user(): User '{user_id}' does not exists", True)
    
    journal.O()
    return toRet

#------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def pgLogin():

    journal.M("/login:")
    return app_views.pgStaged(title='SIQO Homepage', classId='PagManLogin')
    
#------------------------------------------------------------------------------
@app.route('/logout')
def pgLogout():
    
    journal.M("/logout:")
    
    # remove the username from the session if it's there
    session.pop('username', None)

    return redirect(url_for('pgLogin'))

#==============================================================================
# PagMan PATHs operation
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def pgHomepage():

    journal.M("/homepage:")
    return app_views.pgStaged(title='SIQO Homepage', classId='PagManHomepage')

#------------------------------------------------------------------------------
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def pgAdmin():

    journal.M("/admin:")
    return app_views.pgStaged(classId='PagManAdmin')

#------------------------------------------------------------------------------
@app.route('/resource', methods=['GET', 'POST'])
@login_required
def pgResource():

    journal.M("/resource:")
    return app_views.pgStaged(classId='PagManResource')

#------------------------------------------------------------------------------
@app.route('/dms', methods=['GET', 'POST'])
@login_required
def pgDms():

    journal.M("/dms:")
    return app_views.pgStaged(classId='PagManDMS')

#------------------------------------------------------------------------------
@app.route('/session', methods=['GET', 'POST'])
@login_required
def pgSession():

    journal.M("/session:")
    return app_views.pgStaged(classId='PagManSession')

#------------------------------------------------------------------------------
@app.route('/contact', methods=['GET'])
@login_required
def pgContact():

    journal.M("/contact:")
    return app_views.pgStaged(title='SIQO Contacts', classId='PagManContact')

#------------------------------------------------------------------------------
@app.route('/faq',           methods=['GET', 'POST'])
@app.route('/faq/<int:idx>', methods=['GET', 'POST'])
@login_required
def pgFaq(idx=0):

    journal.M(f"/faq:  idx={idx}")
    return app_views.pgStaged(title='SIQO F.A.Q.', classId='FAQ', idx=idx)

#------------------------------------------------------------------------------
# PATHs Tools
#------------------------------------------------------------------------------
@app.get('/user/<username>')
def pgUser(username):

    journal.M(f"/user/username: username='{username}'")

    # show the user profile for that user
    return f"User {escape(username)}"

#------------------------------------------------------------------------------
@app.route('/post/<int:postId>')
def show_post(postId):

    journal.M(f"/post: postId='{postId}'")

    # show the post with the given id, the id is an integer
    return f"Post {postId}"

#------------------------------------------------------------------------------
@app.route('/path/<path:subpath>')
def show_subpath(subpath):

    journal.M(f"/path/subpath: subpath='{subpath}'")

    # show the subpath after /path/
    return f"Subpath {escape(subpath)}"

#==============================================================================
# Custom PATHs operation
#------------------------------------------------------------------------------
@app.route('/oralhistory'          , methods=['GET', 'POST'])
@app.route('/oralhistory/<int:idx>', methods=['GET', 'POST'])
def pgOhistory(idx=0):

    journal.M(f"/oralhistory: idx='{idx}'")
    return app_views.pgStaged(title='SIQO Oral history', classId='OHISTORY', idx=idx)

#------------------------------------------------------------------------------
@app.route('/boc'          , methods=['GET', 'POST'])
@app.route('/boc/<int:idx>', methods=['GET', 'POST'])
def pgBoc(idx=0):

    journal.M(f"/boc: idx='{idx}'")
    return app_views.pgStaged(title='Battle of consistency', classId='PageBOC', idx=idx)

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
with app.test_request_context():
    print('package :', Config.packPath      )
    print('database:', Config.dtbsPath      )
    print('index   :', url_for('index')     )
    print('homepage:', url_for('pgHomepage'))
    
#==============================================================================
print(f"app_routes {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
