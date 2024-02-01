#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   werkzeug.security        import generate_password_hash, check_password_hash
from   flask_login              import UserMixin

import siqo_lib.general         as gen


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_CWD      = os.getcwd()

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
class User(UserMixin):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dtbs):
        "Call constructor of User"

        journal.I(f"User.init: from database '{dtbs.dtbs}'")
        
        #----------------------------------------------------------------------
        self.journal   = journal
        
        self.dtbs      = dtbs
        self.tableName = _DB_TABLE

        self.loaded    = False
        self.changed   = False
        self.verified  = False
        
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
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this user"

        toRet = ''
        for line in self.info: toRet += line +'\n'

        return toRet

    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the user"

        toRet = []

        toRet.append(self.user_id )
        toRet.append(self.password)
        toRet.append(self.fname   )
        toRet.append(self.lname   )
        toRet.append(self.email   )

        return toRet

    #--------------------------------------------------------------------------
    def reset(self):
        
        self.loaded    = False
        self.changed   = False
        self.verified  = False

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
    def authenticate(self, user, pasw):
        
        self.journal.I(f"{self.user_id}.authenticate:")
        
        self.load(user)
        
        #----------------------------------------------------------------------
        # Kontrola existencie usera
        #----------------------------------------------------------------------
        if not self.loaded:
            self.journal.I(f"{self.user_id}.authenticate: User 'user' does not exists")
            self.journal.O()
            return False

        #----------------------------------------------------------------------
        # Kontrola hesla
        #----------------------------------------------------------------------
        if not self.check_password(pasw):
            self.journal.I(f"{self.user_id}.authenticate: Invalid credentials")
            self.journal.O()
            return False

        #----------------------------------------------------------------------
        self.journal.O()
        return True
        
    #==========================================================================
    # Flask login methods
    def is_authenticated(self):
        """This property should return True if the user is authenticated, i.e. 
        they have provided valid credentials. (Only authenticated users will 
        fulfill the criteria of login_required.)"""
        
        return self.verified

    #--------------------------------------------------------------------------
    def is_active(self):
        """This property should return True if this is an active user - 
        in addition to being authenticated, they also have activated their account, 
        not been suspended, or any condition your application has for rejecting an account. 
        Inactive accounts may not log in (without being forced of course)."""

        return self.verified and self.c_func=='A'

    #--------------------------------------------------------------------------
    def is_anonymous(self):
        """This property should return True if this is an anonymous user. 
        (Actual users should return False instead.)"""
        
        return self.user_id == "Anonym"

    #--------------------------------------------------------------------------
    def get_id(self):
        """This method must return a str that uniquely identifies this user, 
        and can be used to load the user from the user_loader callback. 
        Note that this must be a str - if the ID is natively an int or some 
        other type, you will need to convert it to str"""
        
        return self.user_id

    #--------------------------------------------------------------------------
    def set_password(self, password):

#        self.password = generate_password_hash(password)
        self.password = password
        self.changed  = True

    #--------------------------------------------------------------------------
    def check_password(self, password):

        return self.password == password
    
#        return check_password_hash(self.password, password)
    
    #--------------------------------------------------------------------------
        
    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def load(self, user_id):
        
        self.journal.I(f"{self.user_id}.load: user_id = '{user_id}'")
        
        userData = self.dtbs.readTable(user_id, self.tableName, f" user_id = '{user_id}'")
        
        #----------------------------------------------------------------------
        # Skontrolujem existenciu usera
        #----------------------------------------------------------------------
        if len(userData) != 1:
            
            self.loaded   = False
            self.verified = False

            journal.M(f"{self.user_id}.load: User '{user_id}' does not exist")
            self.journal.O()
            return None
        
        #----------------------------------------------------------------------
        self.user_id   = userData[0]['USER_ID'  ]
        self.c_func    = userData[0]['C_FUNC'   ]
        self.lang_id   = userData[0]['LANG_ID'  ]
        self.c_type    = userData[0]['C_TYPE'   ]
        self.fname     = userData[0]['FNAME'    ]
        self.lname     = userData[0]['LNAME'    ]
        self.email     = userData[0]['EMAIL'    ]
        self.password  = userData[0]['PASSWORD' ]
        self.authent   = userData[0]['AUTHENT'  ]
        self.n_fails   = userData[0]['N_FAILS'  ]
        self.d_created = userData[0]['D_CREATED']
        self.d_changed = userData[0]['D_CHANGED']
        self.d_locked  = userData[0]['D_LOCKED' ]
        
        self.loaded = True
        
        self.journal.O()
        return self

    #--------------------------------------------------------------------------
    def save(self, force=False):
        
        self.journal.I(f"{self.user_id}.save: force={force}")
        
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
                self.journal.M(f"{self.user_id}.save: {cnt} row was saved")
                
            else:
                self.journal.M(f"{self.user_id}.save: procedure failed")

        #----------------------------------------------------------------------
        self.journal.O()

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqo_lib                 import SiqoJournal
    journal = SiqoJournal('test-user', debug=5)

    from   database                 import Database
    dtbs = Database(journal, 'test')
    
    user = User(journal, dtbs)
    
    u = user.load('palo4')

#==============================================================================
print(f"User {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
