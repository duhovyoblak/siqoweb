#==============================================================================
#  SIQO Web server: Initialization of the Server
#------------------------------------------------------------------------------
import os

#==============================================================================
# Setting the environment
#------------------------------------------------------------------------------
os.environ['siqo-test'] = '1'
#os.environ['wsiqo-secret-key'] = 'asklurgw8374yhcbfQ2R7GYFQPIUBR'

#==============================================================================
from   siqolib.journal     import SiqoJournal

import app_routes          as app_routes
import app_views           as app_views

#==============================================================================
# package's constants & private vars
#------------------------------------------------------------------------------
_VER      = '1.03'
_CWD      = os.getcwd()

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = SiqoJournal('siqo-web', debug=5)

app_routes.journal = journal
app_views. journal = journal

#==============================================================================
# Get an Flask Application Object
#------------------------------------------------------------------------------
app, login  = app_routes.getApp()

#==============================================================================
# Main
#------------------------------------------------------------------------------
if __name__ =='__main__':
    
    journal.M('Main start')
    
    if _IS_TEST:
        app.run(host='localhost', port=80, debug=True, use_reloader=False)
    
    journal.M('Main end')
    
#==============================================================================
print(f"siqoweb.__init__ {_VER} at {_CWD}")
#                              END OF FILE
#------------------------------------------------------------------------------
