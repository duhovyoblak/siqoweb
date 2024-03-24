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
from   siqo_lib                 import SiqoJournal
import siqo_web.p_views             as vie
import siqo_web.dms                 as dms

import siqo_web.routes              as rou

#==============================================================================
# package's constants & private vars
#------------------------------------------------------------------------------
_VER      = '1.00'
_CWD      = os.getcwd()

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = SiqoJournal('siqo-web', debug=1)

vie.journal = journal
dms.journal = journal
rou.journal = journal

#==============================================================================
# Get an Flask Application Object
#------------------------------------------------------------------------------
app, login  = rou.getApp()

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
