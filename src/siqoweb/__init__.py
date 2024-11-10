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

import app_views           as app_views
import app_dms             as app_dms
import app_routes          as app_routes

#==============================================================================
# package's constants & private vars
#------------------------------------------------------------------------------
_VER      = '1.02'
_CWD      = os.getcwd()

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = SiqoJournal('siqo-web', debug=4)

app_views. journal = journal
app_dms.   journal = journal
app_routes.journal = journal

#==============================================================================
# Get an Flask Application Object
#------------------------------------------------------------------------------
app, login  = app_routes.getApp()

#==============================================================================
# Main
if __name__ =='__main__':
    
    journal.I('Main start')
    
    if _IS_TEST:
        app.run(host='localhost', port=5000, debug=True, use_reloader=False)
    
    journal.O('Main end')
    
#==============================================================================
print(f"wsiqo.__init__ {_VER} at {_CWD}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
