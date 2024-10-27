#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   werkzeug.security        import generate_password_hash, check_password_hash
from   flask_login              import UserMixin

import siqolib.general         as gen
from   database        import Database
from   config          import Config

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
_ANONYM    = 'Anonymous'   # Default user_id for Guest user

#==============================================================================
# Class User
#------------------------------------------------------------------------------
class User(UserMixin, Database):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal):
        "Call constructor of User"

        journal.I("User.init:")
        
        #----------------------------------------------------------------------
        # Konstruktor Database
        #----------------------------------------------------------------------
        super().__init__(journal, Config.dtbsName, Config.dtbsPath)

        #----------------------------------------------------------------------
        self.loaded    = False
        self.changed   = False
        self.verified  = False
        
        self.user_id   = _ANONYM
        self.c_func    = 'L'          #  Users account status: W waiting for authentification A active L locked D deleted */
        self.lang_id   = 'SK'         #  Kod jazyka usera. Platí pre všetky aplikácie */
        self.c_type    = 'P'          #  Users type:A application P person */
        self.fname     = 'Guest'      #  First name */
        self.lname     = 'User'       #  Last name */
        self.email     = ''           #  E-mail address for authentification */
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
        
        return f"User>{' '.join(self.info())}"

    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the user"

        toRet = []

        toRet.append(             self.user_id                  )
        toRet.append(gen.coalesce(self.fname   , 'no_fname'   ) )
        toRet.append(gen.coalesce(self.lname   , 'no_lname'   ) )
        toRet.append(gen.coalesce(self.email   , 'no_email'   ) )
        toRet.append(gen.coalesce(self.password, 'no_password') )

        return toRet

    #--------------------------------------------------------------------------
    def userName(self):
        "Returns name of the user to show"
        
        return f"{self.fname} {self.lname}"
        
    #--------------------------------------------------------------------------
    def reset(self):
        
        self.loaded    = False
        self.changed   = False
        self.verified  = False

        #----------------------------------------------------------------------
        # Len pre istotu nastavim defaultne hodnoty
        #----------------------------------------------------------------------
        self.user_id   = _ANONYM
        self.c_func    = 'L'
        self.lang_id   = 'SK'
        self.c_type    = 'P'
        self.fname     = 'Guest'
        self.lname     = 'User'
        self.email     = ''
        self.password  = 'heslo'
        self.authent   = None
        self.n_fails   = 0
        self.d_created = None
        self.d_changed = None
        self.d_locked  = None
        
    #--------------------------------------------------------------------------
    def authenticate(self, user_id, pasw='?'):
        
        self.journal.I(f"{self.user_id}.authenticate: '{user_id}' with '{pasw}'")
        
        self.load(user_id)
        
        #----------------------------------------------------------------------
        # Kontrola existencie usera
        #----------------------------------------------------------------------
        if not self.loaded:
            self.reset()
            self.journal.M(f"{self.user_id}.authenticate: User 'user_id' does not exists")
            self.journal.O()
            return False

        #----------------------------------------------------------------------
        # Kontrola hesla alebo _ANONYM
        #----------------------------------------------------------------------
        if not (user_id==_ANONYM or self.check_password(pasw)):
            self.reset()
            self.journal.M(f"{self.user_id}.authenticate: Invalid credentials")
            self.journal.O()
            return False

        #----------------------------------------------------------------------
        self.journal.O()
        return True
        
    #==========================================================================
    # Flask login methods
    #--------------------------------------------------------------------------
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
        
        return self.user_id == _ANONYM

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
        
        userData = self.readTable(user_id, table=Config.tabUser, where=f" user_id = '{user_id}'", header='detail')
        
        #----------------------------------------------------------------------
        # Skontrolujem existenciu usera
        #----------------------------------------------------------------------
        if type(userData)==int or len(userData) != 1:
            
            self.reset()
            self.journal.M(f"{self.user_id}.load: User '{user_id}' does not exist")
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
        self.auth_code = userData[0]['AUTH_CODE']
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
            
            sql = f"""UPDATE {Config.tabUser}
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

    #==========================================================================
    # Tools
    #--------------------------------------------------------------------------
    def users(self, header=None):
        "Returns list of users. If failed returns None"
        
        self.journal.I(f"{self.user_id}.users: header={header}")
        
        userLst = self.readTable(who=self.user_id, table=Config.tabUser, header=header)
        
        #----------------------------------------------------------------------
        # Skontrolujem existenciu udajov
        #----------------------------------------------------------------------
        if type(userLst)==int: 
            
            self.journal.M(f"{self.user_id}.users: Method failed, {userLst}", True)
            userLst = None
            
        else:
            self.journal.M(f"{self.user_id}.users: {userLst}")
        
        #----------------------------------------------------------------------
        self.journal.O()
        return userLst

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal       import SiqoJournal
    journal = SiqoJournal('test-user', debug=5)

    user = User(journal)
    users = user.users(header='detail')
    
    u = user.load('palo4')
    print(type(u), ', ', u)

#==============================================================================
print(f"app_user {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
