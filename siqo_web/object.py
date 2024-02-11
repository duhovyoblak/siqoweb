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

_LANG_DEF = 'SK'       # Default language
_SYSUSER  = 'SIQO'     # System superuser

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Class Object
#------------------------------------------------------------------------------
class Object(Database):
    
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
    def __init__(self, journal, page, user, objPar='__PAGE__', rMode= 'STRICT', crForm='Y', lvl=5):
        "Call constructor of Object"

        journal.I("Object.init:")
        
        #----------------------------------------------------------------------
        # Konstruktor Database
        #----------------------------------------------------------------------
        super().__init__(journal, Config.dtbsName, Config.dtbsPath)

        #----------------------------------------------------------------------
        # Identifikacia objektu
        #----------------------------------------------------------------------
        self.name    = f"Object({page}.{objPar})"
        
        self.objPar  = objPar    # Identifikacia parent objektu vramci page
        self.page    = page      # Page, ku ktoremu patri objekt
        self.user    = user      # User, ku ktoremu patri objekt

        self.rMode   = rMode     # uroven kontroly privilegii, STRICT, ROOT

        if self.rMode == 'ROOT': self.objLog = gen.words(self.obj)[0] 
                                 # jednotliva identita (obj)                  pre rMode = 'STRICT'
                                 # skupinova identifikacia objektov word(obj) pre RMode = 'ROOT'
 
        self.uRole   = "Unknown" # Rola usera, priradena k tomuto objektu
        
        self.crForm  = crForm    # vytvaranie formulara, Y, N
  
        self.height  = 10        # vyska content space
        self.width   = 10        # vyska content space
  
        self.items   = []        # zoznam zobrazitelnych poloziek 
        self.btns    = []        # zoznam buttonov

        self.lvl     = lvl       # journal level

        #----------------------------------------------------------------------
        # Verifikujem/registrujem logicky Objekt v databaze
        #----------------------------------------------------------------------
#        self.objectRegister(_SYSUSER)

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
    # Praca s objektom (page-obj)
    #--------------------------------------------------------------------------
    def objectGet(self, who, objPar='__PAGE__'):

        self.journal.I(f"{self.name}.objectGet: For parent '{objPar}'")

        #----------------------------------------------------------------------
        # Inicializacia odpovede
        #----------------------------------------------------------------------
        if objPar == '__PAGE__': toRet = {"__HEAD__":{}, "__NAVB__":{}, "__STAG__":{}}
        else                   : toRet = {}
        
        #----------------------------------------------------------------------
        # Ziskanie stromu objektov
        #----------------------------------------------------------------------
        pag = gen.quoted(self.page)
        par = gen.quoted(objPar   )

        #              0         1          2         3        4            5            6      7
        cols = ('PAGE_ID', 'OBJ_ID', 'OBJ_PAR', 'C_FUNC', 'NOTES', 'D_CREATED', 'D_CHANGED', 'WHO')
        
        sql = f"""select {','.join(cols)} from {Config.tabObj} 
                  where PAGE_ID = {pag} and OBJ_PAR = {par}"""
        
        rows = self.readDb(who, sql)
        
        #----------------------------------------------------------------------
        # Kontrola existencie objektov
        #----------------------------------------------------------------------
        if type(rows)==int or len(rows)==0:
            
            self.journal.M(f"{self.name}.objectGet: No objects for '{objPar}'")
            self.journal.O()
            return toRet

        #----------------------------------------------------------------------
        # Vlozenie dat do stromu
        #----------------------------------------------------------------------
        for row in rows:
            
            #------------------------------------------------------------------
            # Ak je objekt funkcny, vlozim ho do stromu
            #------------------------------------------------------------------
            if row[3] == 'A':
                
                #--------------------------------------------------------------
                # Zzalozenie noveho objektu do stromu
                #--------------------------------------------------------------
                objId = row[1]
                toRet[objId] = {"res":{}, "obj":{}}
                
                self.journal.M(f"{self.name}.objectGet:'{objId}' found")
                
                #--------------------------------------------------------------
                # Ziskam resource k tomuto objektu
                #--------------------------------------------------------------
                res = self.resourceGet(who, objId=objId, )
                toRet[objId]["res"] = res

                #--------------------------------------------------------------
                # Rekurzivnym volanim zistim, ci tento objekt obsahuje vnorene objekty
                #--------------------------------------------------------------
                inObj = self.objectGet(who, objPar=objId)
                
                # Ak existuje vnoreny objetk, tak ho vlozim
                if len(inObj) > 0: toRet[objId]["obj"] = inObj

            #------------------------------------------------------------------

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def objectRegister(self, who):

        self.journal.I(f"{self.name}.objectRegister: for '{who}'")

        pag = gen.quoted(self.page  )
        who = gen.quoted(who        )
        obj = 'd'

        #----------------------------------------------------------------------
        # Verifikacia Objektu v DB
        #----------------------------------------------------------------------
        sql = f"""select C_FUNC from {Config.tabObj}
                  where PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}"""
  
        if self.selectItem(who, sql ):
            
            self.journal.O()
            return

        #----------------------------------------------------------------------
        # Registracia noveho objektu
        #----------------------------------------------------------------------
        sql = f"""insert into {Config.tabObj}
                        ( PAGE_ID, OBJ_ID, C_FUNC, NOTES, D_CREATED, D_CHANGED,     WHO  )
                  values( {pag},   {obj},  'A',   'Automatic register object procedure',
                                                          DATE('now'), DATE('now'), {who})"""
         
        if self.sSql(who, sql) > 0:
            
            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'objectRegister()', 'NO_ACT', 'OK', 
                         stat="automatic object registration" )
        else:
            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'objectRegister()', 'NO_ACT', 'ER', 
                         stat="Object registration failed for pag/obj" )

        #----------------------------------------------------------------------
        self.journal.O()

    #==========================================================================
    # Praca s Resources (page-obj-resource-key)
    #--------------------------------------------------------------------------
    def resourceGet(self, who, objId):
        "Ziskam resource pre tuto kombinaciu page-obj-resource-key"

        self.journal.I(f"{self.name}.resourceGet: obj='{objId}' for '{who}'")
        toRet = {}

        #----------------------------------------------------------------------
        # Ziskanie resource
        #----------------------------------------------------------------------
        pag = gen.quoted(self.page)
        obj = gen.quoted(objId    )
        
        #             0       1        2       3           4           5     6
        cols = ('RES_ID','S_KEY','C_FUNC','S_VAL','D_CREATED','D_CHANGED','WHO')

        sql = f"""select {','.join(cols)} from {Config.tabObjRes}
                  where PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}"""
  
        rows = self.readDb(who, sql)
        self.journal.M(f"{self.name}.resourceGet: '{rows}'")
        
        #----------------------------------------------------------------------
        # Kontrola existencie resource
        #----------------------------------------------------------------------
        if type(rows)==int or len(rows)==0:
            
            self.journal.M(f"{self.name}.resourceGet: No resource for object '{objId}'")
            self.journal.O()
            return toRet
    
        #----------------------------------------------------------------------
        # Vlozim udaje do struktury
        #----------------------------------------------------------------------
        for row in rows:
            
            #------------------------------------------------------------------
            # Ak je resource funkcna, vlozim ju do stromu
            #------------------------------------------------------------------
            if row[2]=='A':
                
                resId = row[0]
                key   = row[1]
                val   = row[3]
                
                if resId not in toRet.keys(): toRet[resId] = {}
                
                toRet[resId][key] = val

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def resourceRegister(self, who, lang, resKey):

        self.journal.I(f"{self.name}.resourceRegister: key='{resKey}' for '{who}' in '{lang}'")

        #----------------------------------------------------------------------
        # Pokusim sa zapisat resource do DB
        #----------------------------------------------------------------------
        pag = gen.quoted(self.page  )
        obj = gen.quoted(self.objLog)
        lan = gen.quoted(lang       )
        key = gen.quoted(resKey     )
        whx = gen.quoted(who        )

        sql = f"""insert into {Object.tabObjRes}
                        ( PAGE_ID, OBJ_ID, LANG_ID, S_KEY, S_VAL,        D_CREATED,   D_CHANGED,   WHO  )
                  values( {pag},   {obj},  {lan},   {key}, '_resource_', DATE('now'), DATE('now'), {whx})"""
         
        #----------------------------------------------------------------------
        # Kontrola vykonania zapisu do DB
        #----------------------------------------------------------------------
        if self.sSQL(who, sql) > 0:
  
            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'resourceRegister()', 'OK', 
                         23, "automatic resource registration" )  

        #----------------------------------------------------------------------
        self.journal.O()

    #==========================================================================
    # Praca s rolami (user-page-obj)
    #--------------------------------------------------------------------------
    def roleGet(self, who):
        "Ziskam rolu usera k objektu z DB. Ak neexistuje, tak rolu zaregistrujem"

        self.journal.I(f"{self.name}.roleGet: for '{who}'")

        #----------------------------------------------------------------------
        # Ak je user SIQO, je automaticky Admin
        #----------------------------------------------------------------------
        if self.user == 'SIQO':

            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj is Admin" ) 
            self.journal.O()
            return 'Admin'
        
        #----------------------------------------------------------------------
        # Ziskam rolu usera k tomuto objektu
        #----------------------------------------------------------------------
        usr = gen.quoted(who         )
        pag = gen.quoted(self.se.page)
        obj = gen.quoted(self.objLog )
  
        sql = f"""select S_ROLE from {Object.tabObjRole}
                  where USER_ID = {usr}
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   C_FUNC  = 'A'"""
  
        role = self.selectItem(self.user, sql)

        #----------------------------------------------------------------------
        # Kontrola existencie role
        #----------------------------------------------------------------------
        if role is not None:

            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj is role" ) 
            self.journal.O()
            return role
    
        else:
            #------------------------------------------------------------------
            # User nema definovanu rolu. Zaregistrujem ho a vratim rolu
            #------------------------------------------------------------------
            role = self.roleRegister(who)

            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj was setted to toRet" ) 

            self.journal.O()
            return role

    #--------------------------------------------------------------------------
    def roleRegister(self, who):
        "Priradim userovi rolu rovnaku aku ma Anonymous ku tomuto objektu"

        self.journal.I(f"{self.name}.roleRegister: for '{who}'")

        #----------------------------------------------------------------------
        # Ziskam rolu usera Anonymous k tomuto objektu
        #----------------------------------------------------------------------
        anonRole = self.roleAnonymGet()

        #----------------------------------------------------------------------
        # Pokus o insert role usera k objektu
        #----------------------------------------------------------------------
        usr = gen.quoted(who        )
        pag = gen.quoted(self.page  )
        obj = gen.quoted(self.objLog)
        rol = gen.quoted(anonRole   )
        who = usr
        
        sql = f"""insert into {Object.tabObjRole} 
                        (USER_ID, PAGE_ID, OBJ_ID, S_ROLE, C_FUNC, D_CREATED,   D_CHANGED,    WHO  )
                  values({usr},   {pag},   {obj},  {rol},  'A',    DATE('now'), DATE('now'), {who})"""

        #----------------------------------------------------------------------
        # Kontrola zapisu do DB
        #----------------------------------------------------------------------
        if self.sSQL(self.user, sql ) > 0:

            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'roleRegister()', 'OK', 
                         20, "automatic role registration" )

        #----------------------------------------------------------------------
        self.journal.O()
        return anonRole

    #--------------------------------------------------------------------------
    def roleAnonymGet(self):

        self.journal.I(f"{self.name}.roleAnonymGet:")

        #----------------------------------------------------------------------
        # Ziskam rolu usera Anonymous k tomuto objektu
        #----------------------------------------------------------------------
        usr = gen.quoted('Anonymous')
        pag = gen.quoted(self.page  )
        obj = gen.quoted(self.objLog)

        sql = f"""select S_ROLE from {Object.tabObjRole}
                  where USER_ID = {usr}
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   C_FUNC  = 'A'"""
  
        role = self.selectItem(self.user, sql)

        #----------------------------------------------------------------------
        # Kontrola existencie role
        #----------------------------------------------------------------------
        if role is not None:

            self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'roleAnonymGet()', 'NO_ACT', 'OK', stat="Anonymous role for pag.obj is role" )
            self.journal.O()
            return role
    
        else:
            #------------------------------------------------------------------
            # Anonymous nema definovanu rolu
            #------------------------------------------------------------------
            self.journal.O()
            return 'Reader'

    #--------------------------------------------------------------------------
    def roleSet(self, who, role, page='ALL_PAGES'):
        "Hromadna zmena role usera"

        self.journal.I(f"{self.name}.roleSet: {role} for {who} in page '{page}'")

        #----------------------------------------------------------------------
        # Pokusim sa updatnut rolu usera k viacerim objektom
        #----------------------------------------------------------------------
        usi = gen.quoted(who )
        roi = gen.quoted(role)
        pai = gen.quoted(page)

        sql = f"""update {Object.tabObjRole}
                  set 
                     S_ROLE    = {roi}
                    ,D_CHANGED = DATE('now')
                    ,WHO       = {usi}
                  where USER_ID = {usi}"""
         
        if page != 'ALL_PAGES': sql += f" and PAGE_ID = '{pai}'"

        #----------------------------------------------------------------------
        # Kontrola vykonania zapisu do DB
        #----------------------------------------------------------------------
        cnt = self.sSQL(who, sql)

        self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'roleSet()', 'OK', 
                       21, "Role roi was set for usi and page pai" )

        #----------------------------------------------------------------------
        self.journal.O()

    #==========================================================================
    # Praca s CACHE (user-page-obj-key)
    #--------------------------------------------------------------------------
    def cacheItem(self, who, orig, key):

        val = self.cacheGet(who, key)
        
        if val is not None: return val
        else              : return orig

    #--------------------------------------------------------------------------
    def cacheGet(self, who, key):

        self.journal.I(f"{self.name}.cacheGet: '{key}' for '{who}'")

        #----------------------------------------------------------------------
        # Ziskanie hodnoty Cache pre existujuci kluc
        #----------------------------------------------------------------------
        obj = gen.quoted(self.objLog)
        usr = gen.quoted(who        )
        pag = gen.quoted(self.page  )
        key = gen.quoted(key        )

        sql = f"""select S_VAL from {Object.tabObjCache}
                  where USER_ID = {usr}
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   S_KEY   = {key}"""
         
        val = self.selectItem(who, sql)

        #----------------------------------------------------------------------
        self.journal.O()
        return val

    #--------------------------------------------------------------------------
    def cacheSet(self, who, key, val):

        self.journal.I(f"{self.name}.cacheSet: '{key}':'{val}' for '{who}'")

        #----------------------------------------------------------------------
        # Update hodnoty Cache do existujuceho kluca
        #----------------------------------------------------------------------
        usr = gen.quoted(who        )
        obj = gen.quoted(self.objLog)
        pag = gen.quoted(self.page  )
        key = gen.quoted(key        )
        val = gen.quoted(val        )

        sql = f"""update {Object.tabObjCache}
                  set S_VAL = {val}, D_CHANGED = DATE('now')
                  where USER_ID = {usr}
                  and   PAGE_ID = {pag}
                  and   OBJ_ID  = {obj}
                  and   S_KEY   = {key}"""
         
        cnt = self.sSQL(who, sql)

        #----------------------------------------------------------------------
        # Kontrola update hodnoty v Cache
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
            if self.sSQL(who, sql) < 1:

                self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'cacheSet()', 'ER', 3, 
                           "key is NOT setted to val" )  
                self.journal.O()
                return

        #----------------------------------------------------------------------
        self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'cacheSet()', 'OK', 
                       38, "key is val" )  

        #----------------------------------------------------------------------
        self.journal.O()

    #--------------------------------------------------------------------------
    def cacheClear(self, who='', page='', obj=''):

        self.journal.I(f"{self.name}.cacheClear: user='{who}', page='{page}', obj='{obj}'")

        #----------------------------------------------------------------------
        # Vymazem definovanu mnozinu cache z DB
        #----------------------------------------------------------------------
        usi = gen.quoted(who )
        pai = gen.quoted(page)
        obi = gen.quoted(obj )

        sql = f"delete from {Object.tabObjCache} where 1=1"
  
        if who  != '': sql += f" and USER_ID = {usi}"
        if page != '': sql += f" and PAGE_ID = {pai}"
        if obj  != '': sql += f" and OBJ_ID  = {obi}"
         
        #----------------------------------------------------------------------
        # Kontrola vymazania cache z DB
        #----------------------------------------------------------------------
        cnt = self.sSQL(who, sql)

        self.sJournal(self.user, 'NO_SESS', self.page, self.name, 'cacheClear()', 'OK', 
                       38, "Cleared row rows for usi-pai-obi"       )  

        #----------------------------------------------------------------------
        self.journal.O()

    #==========================================================================
    # Praca s Autorizaciou
    #--------------------------------------------------------------------------
    def allowPasive(self, who):

        #----------------------------------------------------------------------
        # Ak nejde o stranku, zistim rolu usera vzhladom k objektu
        #----------------------------------------------------------------------
        if self.obj != '__PAGE__': uRole = self.roleGet()
        else                     : uRole = 'Unknown'

        if Object.roleValue[uRole] >= Object.roleValue[self.pRole]: return True
        else                                                      : return False

    #--------------------------------------------------------------------------
    def allowActive(self, who):

        #----------------------------------------------------------------------
        # Ak nejde o stranku, zistim rolu usera vzhladom k objektu
        #----------------------------------------------------------------------
        if self.obj != '__PAGE__': uRole = self.roleGet()
        else                     : uRole = 'Unknown'

        if Object.roleValue[uRole] >= Object.roleValue[self.aRole]: return True
        else                                                      : return False

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqo_lib                 import SiqoJournal
    journal = SiqoJournal('test-object', debug=4)
    
    obj = Object(journal, 'Homepage', 'palo4')
    
    rec = obj.objectGet('ja')
    res = obj.resourceGet('ja', '__HEAD__')


#==============================================================================
print(f"Object {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
