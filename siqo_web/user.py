#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from werkzeug.security          import generate_password_hash, check_password_hash

from   flask_login              import UserMixin
from   database                 import Database

import siqo_lib.general         as gen


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_CWD      = os.getcwd()

_DB_PATH  = f"{_CWD}/database/"
_DB_NAME  = "pagman"
_DB_TABLE = "SUSER"

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Class User
#------------------------------------------------------------------------------
class User(UserMixin, Database):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dtbs, path=''):
        "Call constructor of User"

        journal.I(f"User({dtbs}).init:")
        
        #----------------------------------------------------------------------
        # Zdedeny konstruktor
        #----------------------------------------------------------------------
        super().__init__(journal, dtbs, path)

        #----------------------------------------------------------------------
        self.tableName = _DB_TABLE
        self.loaded    = False
        self.changed   = False
        
        self.user_id   = "Anonym"
        self.c_func    = 'L'          #  Users account status: W waiting for authentification A active L locked D deleted */
        self.lang_id   = 'SK'         #  Kod jazyka usera. Platí pre všetky aplikácie */
        self.c_type    = 'P'          #  Users type:A application P person */
        self.fname     = 'Meno'       #  First name */
        self.lname     = 'Priezvisko' #  Last name */
        self.email     = None         #  E-mail address for authentification */
        self.password  = 'heslo'      #  Password hash
        self.authent   = None         #  Authentification code */
        self.n_fails   = 0            #  failed connections count */
        self.d_created = None         #  creations date */
        self.d_changed = None         #  Date of last connection */
        self.d_locked  = None         #  Meta last chage date */
        
        self.journal.O()
        
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def reset(self):
        
        self.loaded    = False

        #----------------------------------------------------------------------
        # Len pre istotu nastavim defaultne hodnoty
        #----------------------------------------------------------------------
        self.user_id   = "Anonym"
        self.c_func    = 'L'
        self.lang_id   = 'SK'
        self.c_type    = 'P'
        self.fname     = 'Meno'
        self.lname     = 'Priezvisko'
        self.email     = None
        self.password  = 'heslo'
        self.authent   = None
        self.n_fails   = 0
        self.d_created = None
        self.d_changed = None
        self.d_locked  = None
        
#--------------------------------------------------------------------------
    def set_password(self, password):

        self.password = generate_password_hash(password)
        self.changed  = True

    #--------------------------------------------------------------------------
    def check_password(self, password):

        return check_password_hash(self.password, password)
    
    #--------------------------------------------------------------------------
        
    #==========================================================================
    # API for users
    #--------------------------------------------------------------------------
    def authenticate(self, user, passw):
        
        journal.I(f"{self.user_id}@{self.dtbs}.authenticate:")

        self.journal.O()
        
    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def load(self, user):
        
        journal.I(f"{self.user_id}@{self.dtbs}.load: {user}")


        self.journal.O()
        
    #--------------------------------------------------------------------------
    def save(self, force=False):
        
        journal.I(f"{self.user_id}@{self.dtbs}.save: force={force}")
        
        #----------------------------------------------------------------------
        # Ak nastala zmena udajov alebo je save vynutene
        #----------------------------------------------------------------------
        if self.changed or force:
            
            sql = f"""UPDATE {self.tableName}
set
 user_id   = {self.user_id}
,c_func    = {self.c_func }
,lang_id   = {self.lang_id}
,c_type    = {self.c_type}
,fname     = {self.fname}
,lname     = {self.lname}
,email     = {self.email}
,password  = {self.password}
,authent   = {self.authent}
,n_fails   = {self.n_fails}
,d_created = {self.d_created}
,d_changed = now()
,d_locked  = {self.d_locked}
where user_id = {self.user_id}"""

            cnt = self.sSql(self.user_id, sql)
            
            #------------------------------------------------------------------
            # Skontrolujem, kolko riadkov sa zmenilo
            #------------------------------------------------------------------
            if cnt > 0:
                self.changed = False
                journal.M(f"{self.user_id}@{self.dtbs}.save: {cnt} row was saved")
                
            else:
                journal.M(f"{self.user_id}@{self.dtbs}.save: procedure failed")

        #----------------------------------------------------------------------
        self.journal.O()

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqo_lib    import SiqoJournal
    journal = SiqoJournal('test-user', debug=5)
    
    user = User(journal, _DB_NAME, _DB_PATH)
    
#    user.createDb(who="who")
#    user.sSqlScript('who', fName='pagman.ini')

    u = user.load('palo4')

#==============================================================================
print(f"User {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
