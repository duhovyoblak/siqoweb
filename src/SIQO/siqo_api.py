#==============================================================================
#  SIQO Homepage: web API
#------------------------------------------------------------------------------
import os

from   flask                    import Flask, request

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_THIS_IS_TEST  = True if os.environ['siqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
app = Flask(__name__)

#==============================================================================
# package's tools
#------------------------------------------------------------------------------
def shutdown_server():
    'Tu by chcelo stop'
    
#==============================================================================
# PATHs operation
#------------------------------------------------------------------------------
@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
