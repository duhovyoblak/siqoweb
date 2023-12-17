#==============================================================================
#  SIQO Homepage: main file
#------------------------------------------------------------------------------
import os

os.environ['siqo-test-mode'] = '1'

from jinja2          import Environment, PackageLoader, select_autoescape

from siqo_journal    import SiqoJournal
from siqo_api        import app

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_THIS_IS_TEST  = True if os.environ['siqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
env = Environment(
    
    loader     = PackageLoader("main"),
    autoescape = select_autoescape()
)

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# Functions
#------------------------------------------------------------------------------
if __name__ =='__main__':

    journal = SiqoJournal('SIQO Homepage', debug=5)
    journal.I('Main start')

    app.run(host='localhost', port=5000, debug=True, use_reloader=False)
    
    journal.O('Main end')
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
