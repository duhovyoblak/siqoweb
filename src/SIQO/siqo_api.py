#==============================================================================
#  SIQO Homepage: web API
#------------------------------------------------------------------------------
import os

from   flask                    import Flask, url_for, render_template, make_response
from   flask                    import request, session, abort, redirect
from   markupsafe               import escape

import jinja2 as j2
import homepage as hp

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_IS_TEST  = True if os.environ['siqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
app = Flask('SIQO')   # 'SIQO' je folder pre celu Homepage

app.secret_key = b'_5#34gvaebh y\xec]/'

#==============================================================================
# package's tools
#------------------------------------------------------------------------------
def shutdown_server():
    'Tu by chcelo stop'
    pass
    
@app.errorhandler(404)
def page_not_found(error):
    
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'

    return resp

#Note the 404 after the render_template() call. This tells Flask that the status code of that page should be 404 which means not found. By default 200 is assumed which translates to: all went well.


#@app.before_request
#==============================================================================
# PATHs operation
#------------------------------------------------------------------------------
@app.get("/")
def index():
    return hp.index()

#------------------------------------------------------------------------------
@app.get('/homepage')
def homepage():
    return hp.homepage()
    
#------------------------------------------------------------------------------
@app.get('/shutdown')
def shutdown():
    abort(404)
    shutdown_server()
    return 'Server shutting down...'

#------------------------------------------------------------------------------
@app.get('/login')
def login_page():
    return '''
    <form method="post">
        <p><input type=text name=username>
        <p><input type=submit value=Login>
    </form>
'''

#------------------------------------------------------------------------------
@app.post('/login')
def login_user():
 
    session['username'] = request.form['username']
    return redirect(url_for('index'))

#------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

#------------------------------------------------------------------------------
@app.get('/user/<username>')
def profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

#------------------------------------------------------------------------------
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

#------------------------------------------------------------------------------
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login_page'))
    print(url_for('login_user'))
    print(url_for('profile', username='John Doe'))
    print(url_for('static', filename='base_page.css'))
    
#==============================================================================
print(f"siqo_api {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
