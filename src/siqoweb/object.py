#==============================================================================
#  SIQO web library: def for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   werkzeug.security        import generate_password_hash, check_password_hash
from   flask_login              import UserMixin

import siqolib.general         as gen
from   config          import Config
from   database        import Database
from   dms             import DMS

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.01'

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
    def __init__(self, journal, user, classId, objPar='__PAGE__', rMode= 'STRICT', crForm='Y', lvl=5):
        "Call constructor of Object"

        journal.I("Object.init:")
        
        #----------------------------------------------------------------------
        # Konstruktor Database
        #----------------------------------------------------------------------
        super().__init__(journal, Config.dtbsName, Config.dtbsPath)

        #----------------------------------------------------------------------
        # Identifikacia objektu
        #----------------------------------------------------------------------
        self.name    = f"Object({classId}.{objPar})"
        self.user    = user      # User, ku ktoremu patri objekt
        
        self.objPar  = objPar    # Identifikacia parent objektu vramci page
        self.classId = classId   # Typ objektu/Page, ku ktoremu patri objekt

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
        
        self.ssbPos  = 1         # Pozicia polozky Stage Selectora

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
    def objectGet(self, who, objPar):
        "Returns dict of obects {objId:{'items':[{}], 'objs':{}}}"
#!!!! znacka
        self.journal.I(f"{self.name}.objectGet: For parent '{objPar}'")

        # objs = { objId = {'items':[ {itemId:{attributes}} ], 'objs':{objs} } }

        #----------------------------------------------------------------------
        # Inicializacia odpovede
        #----------------------------------------------------------------------
        toRet = {}
        
        #----------------------------------------------------------------------
        # Priprava podmienky pre citanie db
        #----------------------------------------------------------------------
        pagStr = gen.quoted(self.classId)
        parStr = gen.quoted(objPar)
        
        # Ak je parent najvyssej urovne upravim podmienku
        if objPar[0:2] == '__' and objPar[-1] == '_': parCond =  "SUBSTR(OBJ_PAR, 1, 2) = '__'"
        else                                        : parCond = f"OBJ_PAR = {parStr}"
 
        #              0         1          2         3        4            5            6      7
        cols = ('CLASS_ID', 'OBJ_ID', 'OBJ_PAR', 'C_FUNC', 'NOTES', 'D_CREATED', 'D_CHANGED', 'WHO')
        
        #----------------------------------------------------------------------
        # Ziskanie stromu objektov
        #----------------------------------------------------------------------
        sql = f"""select {','.join(cols)} from {Config.tabObj} 
                  where CLASS_ID = {pagStr} and {parCond}
                  order by OBJ_PAR, OBJ_ID"""
        
        #self.journal.M(f"{self.name}.objectGet: {sql}")
        rows = self.readDb(who, sql)
        
        #----------------------------------------------------------------------
        # Kontrola existencie objektov
        #----------------------------------------------------------------------
        if type(rows)==int or len(rows)==0:
            
            self.journal.M(f"{self.name}.objectGet: No objects for '{objPar}'")
            self.journal.O()
            return toRet

        #self.journal.M(f"{self.name}.objectGet: Rows for analysis {rows}")

        #----------------------------------------------------------------------
        # Vlozenie dat do stromu
        #----------------------------------------------------------------------
        prevParId = ''
        obj = {"items":[], "objs":{}}

        for row in rows:

            #------------------------------------------------------------------
            # Ak je objekt funkcny
            #------------------------------------------------------------------
            if row[3] == 'A':
                
                #--------------------------------------------------------------
                # Ziskam nazov a parenta objektu
                #--------------------------------------------------------------
                objId = row[1]
                parId = row[2]
                self.journal.M(f"{self.name}.objectGet:'{objId}' in parent '{parId}' found")
                
                #--------------------------------------------------------------
                # Ziskam resource k parent objektu
                #--------------------------------------------------------------
                items = self.resourceGet(who, objId=objId)
                obj["items"].extend(items)
                self.journal.M(f"{self.name}.objectGet: resource for '{objPar}' are '{items}'")

                #--------------------------------------------------------------
                # Rekurzivnym volanim zistim, ci tento objekt obsahuje vnorene objekty
                #--------------------------------------------------------------
#                inObjs = self.objectGet(who, objPar=objId)
                
                # Ak existuju vnorene objekty, tak ich vlozim
#                if len(inObjs) > 0: obj["objs"] = inObjs

                #--------------------------------------------------------------
                # Ak je to novy parId, vlozim objekt do zoznamu a resetnem analyzu
                #--------------------------------------------------------------
                if prevParId != parId:
                    
                    self.journal.M(f"{self.name}.objectGet: Analyse of parent '{parId}' ended")
                    
                    #----------------------------------------------------------
                    # Ulozim objekt pod klucom parenta
                    #----------------------------------------------------------
                    toRet[parId] = obj
                    
                    #----------------------------------------------------------
                    # Resetnem analyzu pre nasledujuci objekt
                    #----------------------------------------------------------
                    prevParId = parId
                    obj = { "items":[], "objs":{} }
                    
        #----------------------------------------------------------------------
        # Dokoncim vlozenie posledneho objektu
        #----------------------------------------------------------------------
        if prevParId != '': toRet[prevParId] = obj

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def objectRegister(self, who):

        self.journal.I(f"{self.name}.objectRegister: for '{who}'")

        pag = gen.quoted(self.classId  )
        who = gen.quoted(who        )
        obj = 'd'

        #----------------------------------------------------------------------
        # Verifikacia Objektu v DB
        #----------------------------------------------------------------------
        sql = f"""select C_FUNC from {Config.tabObj}
                  where CLASS_ID = {pag}
                  and   OBJ_ID   = {obj}"""
  
        if self.selectItem(who, sql ):
            
            self.journal.O()
            return

        #----------------------------------------------------------------------
        # Registracia noveho objektu
        #----------------------------------------------------------------------
        sql = f"""insert into {Config.tabObj}
                        ( CLASS_ID, OBJ_ID, C_FUNC, NOTES, D_CREATED, D_CHANGED,     WHO  )
                  values( {pag},   {obj},  'A',   'Automatic register object procedure',
                                                          DATE('now'), DATE('now'), {who})"""
         
        if self.sSql(who, sql) > 0:
            
            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'objectRegister()', 'NO_ACT', 'OK', 
                         stat="automatic object registration" )
        else:
            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'objectRegister()', 'NO_ACT', 'ER', 
                         stat="Object registration failed for pag/obj" )

        #----------------------------------------------------------------------
        self.journal.O()

    #==========================================================================
    # Praca s Resources (page-obj-resource-key)
    #--------------------------------------------------------------------------
    def resourceGet(self, who, objId):
        "Returns list of items for keys page-obj"
#!!!! znacka

        self.journal.I(f"{self.name}.resourceGet: obj='{objId}' for '{who}'")
        toRet = []

        #----------------------------------------------------------------------
        # Ziskanie resource
        #----------------------------------------------------------------------
        pag = gen.quoted(self.classId)
        obj = gen.quoted(objId    )
        
        #              0       1        2       3           4           5     6
        cols = ('ITEM_ID','S_KEY','C_FUNC','S_VAL','D_CREATED','D_CHANGED','WHO')

        sql = f"""select {','.join(cols)} from {Config.tabObjRes}
                  where CLASS_ID = {pag} and   OBJ_ID  = {obj}
                  order by ITEM_ID"""
  
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
        # Vlozim udaje do struktury [ {item:{}} ]
        #----------------------------------------------------------------------
        prevItemId = ''
        itemId     = ''
        item       = {}

        for row in rows:
            #------------------------------------------------------------------
            # Ak je resource funkcna, vlozim ju do stromu
            #------------------------------------------------------------------
            if row[2]=='A':
                
                itemId = row[0]
                key    = row[1]
                val    = row[3]

                #--------------------------------------------------------------
                # Ak je key = SBB potom vygenerujem polozku Stage selectora
                #--------------------------------------------------------------
                if key == 'SSB' and False:
                    
                    key     = 'SK'
                    itemId  = f'SSB_{self.ssbPos}'
                    self.ssbPos += 1

                #--------------------------------------------------------------
                # Ak je to novy itemId, vlozim predchadzajuci do zoznamu a resetnem item
                #--------------------------------------------------------------
                if prevItemId != itemId:
                    
                    if prevItemId != '': toRet.append(item)
                    
                    prevItemId = itemId
                    item = {itemId:{}}
                    
                #--------------------------------------------------------------
                # Akumulujem atributy aktualneho itemu
                #--------------------------------------------------------------
                item[itemId][key] = val

            #------------------------------------------------------------------

        #----------------------------------------------------------------------
        # Dokoncim vlozenie posledneho objektu
        #----------------------------------------------------------------------
        if itemId != '': toRet.append(item)

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def resourceRegister(self, who, lang, resKey):

        self.journal.I(f"{self.name}.resourceRegister: key='{resKey}' for '{who}' in '{lang}'")

        #----------------------------------------------------------------------
        # Pokusim sa zapisat resource do DB
        #----------------------------------------------------------------------
        pag = gen.quoted(self.classId  )
        obj = gen.quoted(self.objLog)
        lan = gen.quoted(lang       )
        key = gen.quoted(resKey     )
        whx = gen.quoted(who        )

        sql = f"""insert into {Object.tabObjRes}
                        ( CLASS_ID, OBJ_ID, LANG_ID, S_KEY, S_VAL,        D_CREATED,   D_CHANGED,   WHO  )
                  values( {pag},   {obj},  {lan},   {key}, '_resource_', DATE('now'), DATE('now'), {whx})"""
         
        #----------------------------------------------------------------------
        # Kontrola vykonania zapisu do DB
        #----------------------------------------------------------------------
        if self.sSQL(who, sql) > 0:
  
            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'resourceRegister()', 'OK', 
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

            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'roleGet()', 'OK', 
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

            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj is role" ) 
            self.journal.O()
            return role
    
        else:
            #------------------------------------------------------------------
            # User nema definovanu rolu. Zaregistrujem ho a vratim rolu
            #------------------------------------------------------------------
            role = self.roleRegister(who)

            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'roleGet()', 'OK', 
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
        pag = gen.quoted(self.classId  )
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

            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'roleRegister()', 'OK', 
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
        pag = gen.quoted(self.classId  )
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

            self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'roleAnonymGet()', 'NO_ACT', 'OK', stat="Anonymous role for pag.obj is role" )
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

        self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'roleSet()', 'OK', 
                       21, f"Role roi was set for usi and page pai {cnt}" )

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
        pag = gen.quoted(self.classId  )
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
        pag = gen.quoted(self.classId  )
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

                self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'cacheSet()', 'ER', 3, 
                           "key is NOT setted to val" )  
                self.journal.O()
                return

        #----------------------------------------------------------------------
        self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'cacheSet()', 'OK', 
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

        self.sJournal(self.user, 'NO_SESS', self.classId, self.name, 'cacheClear()', 'OK', 
                       38, f"Cleared {cnt} row(s)"       )  

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
    
    from   siqolib.journal                 import SiqoJournal
    journal = SiqoJournal('test-object', debug=3)
    
    obj = Object(journal, 'palo4', 'Homepage')
    
    rec = obj.objectGet('ja')
    #res = obj.resourceGet('ja', '__STAG__')


#==============================================================================
print(f"Object {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
