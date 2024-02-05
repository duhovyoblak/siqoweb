#==============================================================================
#  SIQO web library: def for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   werkzeug.security        import generate_password_hash, check_password_hash
from   flask_login              import UserMixin

import siqo_lib.general         as gen
from   siqo_web.database        import Database
from   siqo_web.config          import Config

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.00'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Class Object
#------------------------------------------------------------------------------
class Object(Database):
    
    tabObj      = Config.tabObject
    tabObjRes   = Config.tabObjRes
    tabObjRole  = Config.tabObjRole
    tabObjCache = Config.tabObjCache

    roleValue = { "__ERRORR__" : 0
                 ,"Unknown"    : 0
                 ,"Reader"     : 1
                 ,"User"       : 2
                 ,"Writer"     : 3
                 ,"Admin"      : 4
                }
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal,  obj, aRole, pRole, rMode= 'STRICT', crForm='Y', lvl=38):
        "Call constructor of Object"

        journal.I("Object.init:")
        
        #----------------------------------------------------------------------
        # Konstruktor Database
        #----------------------------------------------------------------------
        super().__init__(journal, Config.dtbsName, Config.dtbsPath)

        #----------------------------------------------------------------------
        # Identifikacia objektu
        #----------------------------------------------------------------------
        self.obj     = obj       # jednoznacna identifikacia objektu
        self.objRoot = ''        # skupinova identifikacia objektov pre RMode = 'ROOT'
 
        self.aRole   = aRole     # Vyzadovana rola pre aktivne operacie
        self.pRole   = pRole     # Vyzadovana rola pre pasivne operacie
        self.uRole   = "Unknown" # Rola usera, priradena k tomuto objektu
        
        self.rMode   = rMode     # uroven kontroly privilegii, STRICT, ROOT
        self.crForm  = crForm    # vytvaranie formulara, Y, N
  
        self.height  = 10        # vyska content space
        self.width   = 10        # vyska content space
  
        self.items   = []        # zoznam zobrazitelnych poloziek 
        self.btns    = []        # zoznam buttonov

        self.lvl     = lvl       # journal level

        #----------------------------------------------------------------------
        if self.rMode == 'ROOT': self.objRoot = word( self.obj, 0) 

        #----------------------------------------------------------------------
        # Verifikujem unikatny a genericky Objekt vzhladom k databaze
        #----------------------------------------------------------------------
        if self.rMode == 'STRICT': self.ObjectRegister()
        else                     : self.ObjectRegister(self.objRoot)

        #----------------------------------------------------------------------
        # Ak nejde o stranku, zistim rolu usera vzhladom k objektu
        #----------------------------------------------------------------------
        if self.obj != '__PAGE__': self.URole = self.RoleGet()

        #----------------------------------------------------------------------
        self.journal.O()
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Object"
        
        return f"Object>{' '.join(self.info())}"

    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the Object"

        toRet = []

        return toRet

    #==========================================================================
    # Praca s Autorizaciou
    #--------------------------------------------------------------------------
    def allowPasive(self, task = ''):

        if Object.roleValue[self.URole] >= Object.roleValue[self.pRole]: return True
        else                                                           : return False

    #--------------------------------------------------------------------------
    def allowActive(self, task = ''):

        if Object.roleValue[self.URole] >= Object.roleValue[self.aRole]: return True
        else                                                           : return False

    #--------------------------------------------------------------------------
    # Praca s rolami
    #--------------------------------------------------------------------------
    def roleRegister(self):

        journal.I(f"{self.name}.roleRegister:")

        anonRole = self.roleAnonymGet()

        pag = gen.quoted(self.se.page)
        usr = gen.quoted(self.se.user)
        rol = gen.quoted(anonRole    )
 
        if self.rMode == 'STRICT': obj = gen.quoted(self.obj    )
        else                     : obj = gen.quoted(self.objRoot)
        
        #----------------------------------------------------------------------
        # pokus o insert role k objektu
        #----------------------------------------------------------------------
        sql = f"""insert into {Object.tabObjRole} 
                        (USER_ID, PAGE_ID, OBJ_ID, S_ROLE, C_FUNC, D_CREATED,   D_CHANGED,   WHO  )
                  values({usr},   {pag},   {obj},  {rol},  'A',    DATE('now'), DATE('now'), {usr})"""

        if self.sSQL( self.se, sql ) > 0:

            self.se.JournalS( self.obj, 'S_Object.php', 'roleRegister()', 'OK', 
                         20, "automatic role registration" )

        #----------------------------------------------------------------------
        return anonRole

    #--------------------------------------------------------------------------
    def roleGet(self):

        #----------------------------------------------------------------------
        # Priprava
        #----------------------------------------------------------------------
        usr = gen.quoted(self.se.user)
        pag = gen.quoted(self.se.page)
  
        if self.rMode == 'STRICT': obj = gen.quoted(self.obj    )
        else                     : obj = gen.quoted(self.objRoot)

        #----------------------------------------------------------------------
        # Ak je user SIQO, je automaticky Admin
        #----------------------------------------------------------------------
        if self.se.user == 'SIQO':

            self.se.JournalS( self.obj, 'S_Object.php', 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj is Admin" ) 
            return 'Admin'
  
        #----------------------------------------------------------------------
        # Konstrukcia selectu
        #----------------------------------------------------------------------
        sql = f"""select S_ROLE from {Object.tabObjRole}
                  where USER_ID = {usr}
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   C_FUNC  = 'A'"""
  
        #----------------------------------------------------------------------
        # Odcitanie role pre USERa
        #----------------------------------------------------------------------
        role = self.selectItem(self.se, sql)
        if role is not None:

            self.se.JournalS( self.obj, 'S_Object.php', 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj is role" ) 
            return role
    
        else:
            #------------------------------------------------------------------
            # USER nema definovanu rolu. Zaregistrujem a vratim rolu pre Anonymous  
            #------------------------------------------------------------------
            toRet = self.roleRegister()

            self.se.JournalS( self.obj, 'S_Object.php', 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj was setted to toRet" ) 

            return toRet

    #--------------------------------------------------------------------------
    def roleAnonymGet(self):

        #----------------------------------------------------------------------
        # Konstrukcia selectu
        #----------------------------------------------------------------------
        pag = gen.quoted(self.se.page )
  
        if self.rMode == 'STRICT': obj = gen.quoted(self.obj    )
        else                     : obj = gen.quoted(self.objRoot)

        sql = f"""select S_ROLE from {Object.tabObjRole}
                  where USER_ID = 'Anonymous'
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   C_FUNC  = 'A'"""
  
        #----------------------------------------------------------------------
        # Odcitanie role
        #----------------------------------------------------------------------
        role = self.selectItem(self.se, sql)
        if role is not None:

            self.se.JournalS( self.obj, 'S_Object.php', 'roleAnonymGet()', 'OK', 
                         22, "Anonymous role for pag.obj is role" ) 
            return role
    
        else:
            return 'Reader'

    #--------------------------------------------------------------------------
    def roleSet(self, user, role, page=''):

        usi = gen.quoted(user )
        roi = gen.quoted(role )
        pai = gen.quoted(page )
        who = gen.quoted(self.se.user )

        #----------------------------------------------------------------------
        # pokus o update
        #----------------------------------------------------------------------
        sql = f"""update {Object.tabObjRole}
                  set 
                     S_ROLE    = {roi}
                    ,D_CHANGED = DATE('now')
                    ,WHO       = {who}
                  where USER_ID = {usi}"""
         
        if page != '': sql += f" and PAGE_ID = '{pai}'"

        cnt = self.sSQL( self.se, sql )

        self.se.JournalS( self.obj, 'S_Object.php', 'roleSet()', 'OK', 
                       21, "Role roi was set for usi and page pai" )

    #--------------------------------------------------------------------------
    # Praca s Resources
    #--------------------------------------------------------------------------
    def resourceRegister(self, resCode):

        usr = gen.quoted(self.se.user )
        pag = gen.quoted(self.se.page )
        lan = gen.quoted(self.se.lang )
        res = gen.quoted(resCode      )

        if self.rMode == 'STRICT': obj = gen.quoted(self.obj    )
        else                     : obj = gen.quoted(self.objRoot)

        #----------------------------------------------------------------------
        # pokus o insert
        #----------------------------------------------------------------------
        sql = f"""insert into {Object.tabObjRes}
                        ( PAGE_ID, OBJ_ID, LANG_ID, S_KEY, S_VAL,        D_CREATED,   D_CHANGED,   WHO  )
                  values( {pag},   {obj},  {lan},   {res}, '_resource_', DATE('now'), DATE('now'), {usr})"""
         
        if self.sSQL( self.se, sql ) > 0:
  
            self.se.JournalS( self.obj, 'S_Object.php', 'resourceRegister()', 'OK', 
                         23, "automatic resource registration" )  

    #--------------------------------------------------------------------------
    def resourceGet(self, resCode ):

        pag = gen.quoted(self.se.page )
        lan = gen.quoted(self.se.lang )
        res = gen.quoted(resCode      )

        if self.rMode == 'STRICT': obj = gen.quoted(self.obj    )
        else                     : obj = gen.quoted(self.objRoot)

        sql = f"""select S_VAL from {Object.tabObjRes}
                  where PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   LANG_ID = {lan}
                  and   S_KEY   = {res}"""
  
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        val = self.selectItem(self.se, sql)
        
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        if val is not None:
            self.se.JournalS( self.obj, 'S_Object.php', 'resourceGet()', 'OK', 
                            24, "resource for pag.obj.lan.res is val" ) 
            return val
    
        else:
            #------------------------------------------------------------------
            # Ak sa nepodarilo ziskat value, zaregistrujeme kluc resource
            #------------------------------------------------------------------
            self.se.JournalS( self.obj, 'S_Object.php', 'resourceGet()', 'SW', 
                         24, "no resource for pag.obj.lan.res" )
                         
            self.resourceRegister(resCode)
            return '__NO_RESOURCE__'

    #--------------------------------------------------------------------------
    # Praca s CACHE
    #--------------------------------------------------------------------------
    def cacheSet(self, key, val):

        if self.rMode == 'STRICT': obj = gen.quoted(self.obj    )
        else                     : obj = gen.quoted(self.objRoot)

        usr = gen.quoted(self.se.user )
        pag = gen.quoted(self.se.page )
        key = gen.quoted(key          )
        val = gen.quoted(val          )

        #----------------------------------------------------------------------
        # Update hodnoty Cache do existujuceho kluca
        #----------------------------------------------------------------------
        sql = f"""update {Object.tabObjCache}
                  set S_VAL = {val}, D_CHANGED = DATE('now')
                  where USER_ID = {usr}
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   S_KEY   = {key}"""
         
        cnt = self.sSQL( self.se, sql )

        #----------------------------------------------------------------------
        # Update hodnoty v Cache - test uspesnosti
        #----------------------------------------------------------------------
        if cnt < 1:

            #------------------------------------------------------------------
            # Zapis hodnoty do noveho kluca v Cache
            #------------------------------------------------------------------
            sql = f"""insert into {Object.tabObjCache}
                            ( USER_ID, PAGE_ID, OBJ_ID, S_KEY, S_VAL, D_CHANGED   )
                      values( {usr},   {pag},   {obj},  {key}, {val}, DATE('now') )"""
    
            #------------------------------------------------------------------
            # Test zlyhania insertu
            #------------------------------------------------------------------
            if self.sSQL( self.se, sql ) < 1:

                self.se.JournalS( self.obj, 'S_Object.php', 'cacheSet()', 'ER', 3, 
                           "key is NOT setted to val" )  
                return

        #----------------------------------------------------------------------
        self.se.JournalS( self.obj, 'S_Object.php', 'cacheSet()', 'OK', 
                       38, "key is val" )  

    #--------------------------------------------------------------------------
    def cacheGet(self, key ):

        if self.rMode == 'STRICT': obj = gen.quoted(self.obj    )
        else                     : obj = gen.quoted(self.objRoot)

        usr = gen.quoted(self.se.user )
        pag = gen.quoted(self.se.page )
        key = gen.quoted(key          )

        sql = f"""select S_VAL from {Object.tabObjCache}
                  where USER_ID = {usr}
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   S_KEY   = {key}"""
         
        toRet = self.selectItem( self.se, sql )
        return toRet

    #--------------------------------------------------------------------------
    def cacheItem(self, orig, key ):

        pom = self.cacheGet( key )
        
        if pom != '': return pom
        else        : return orig

    #--------------------------------------------------------------------------
    def cacheClear(self, user='', page='', obj='' ):

        usi = gen.quoted(user )
        pai = gen.quoted(page )
        obi = gen.quoted(obj  )

        #----------------------------------------------------------------------
        # pokus o delete
        #----------------------------------------------------------------------
        sql = f"delete from {Object.tabObjCache} where 1=1"
  
        if user != '': sql += f" and USER_ID = {usi}"
        if page != '': sql += f" and PAGE_ID = {pai}"
        if obj  != '': sql += f" and OBJ_ID  = {obi}"
         
        cnt = self.sSQL( self.se, sql )

        self.se.JournalS( self.obj, 'S_Object.php', 'cacheClear()', 'OK', 
                       38, "Cleared row rows for usi-pai-obi"       )  

    #--------------------------------------------------------------------------
    # Registracia objeku
    #--------------------------------------------------------------------------
    def objectRegister(self, obj = '' ):

        pag = gen.quoted(self.se.page )
        usr = gen.quoted(self.se.user )
  
        if  obj == '': obj = gen.quoted(self.obj )
        else         : obj = gen.quoted(obj      )

        #----------------------------------------------------------------------
        # Verifikacia Objektu v DB
        #----------------------------------------------------------------------
        sql = f"""select C_FUNC from {Object.tabObj}
                  where PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}"""
  
        if self.selectItem( self.se, sql ): return

        #----------------------------------------------------------------------
        # Registracia noveho objektu
        #----------------------------------------------------------------------
        sql = f"""insert into {Object.tabObj}
                        ( PAGE_ID, OBJ_ID, C_FUNC, NOTES, D_CREATED, D_CHANGED,     WHO  )
                  values( {pag},   {obj},  'A',   'Automatic register object procedure',
                                                          DATE('now'), DATE('now'), {usr})"""
         
        if self.sSQL( self.se, sql ) > 0:
            
            self.se.JournalS( self.obj, 'S_Object.php', 'objectRegister()', 'OK', 
                         25, "automatic object registration" )
        else:
            self.se.JournalS( self.obj, 'S_Object.php', 'objectRegister()', 'ER', 
                         2, "Object registration failed for pag/obj" )

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqo_lib                 import SiqoJournal
    journal = SiqoJournal('object-user', debug=5)


#==============================================================================
print(f"Object {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
