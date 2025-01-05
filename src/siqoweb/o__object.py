#==============================================================================
#  SIQO web library: def for SIQO Flask application
#------------------------------------------------------------------------------
from   werkzeug.security     import generate_password_hash, check_password_hash
from   flask_login           import UserMixin

import siqolib.general       as gen
from   config                import Config
from   html_render           import HTML

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.06'

_LANG_DEF = 'SK'       # Default language
_SYSUSER  = 'SIQO'     # System superuser

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Class Object
#------------------------------------------------------------------------------
class Object(HTML):
    
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
    def __init__(self, journal, dms, userId, lang, classId, objPar=None, height='20%', width='20%'):
        "Call constructor of Object"

        journal.I("Object.init:")

        #----------------------------------------------------------------------
        # Inicializacia HTML renderera
        #----------------------------------------------------------------------
        super().__init__(journal, userId, lang, classId)  # classId=OBJECT_ID v pagman db

        #----------------------------------------------------------------------
        # Identifikacia objektu
        #----------------------------------------------------------------------
        self.name    = f"Object({objPar})"
        self.dms     = dms       # DMS/Database
        self.height  = height
        self.width   = width
        
        self.conts   = []        # obsah objektu [{item}, {item}, <Object>, {item}, ...] 

        self.rMode   = 'ROOT'    # uroven kontroly privilegii, STRICT, ROOT
#        if self.rMode == 'ROOT': self.objLog = gen.words(self.obj)[0] 
                                 # jednotliva identita (obj)                  pre rMode = 'STRICT'
                                 # skupinova identifikacia objektov word(obj) pre RMode = 'ROOT'
 
        self.uRole   = "Unknown" # Rola usera, priradena k tomuto objektu

        #----------------------------------------------------------------------
        # Verifikujem/registrujem logicky Objekt v databaze
        #----------------------------------------------------------------------
#        self.objectRegister(_SYSUSER)

        #----------------------------------------------------------------------
        # Ak je zadany parent Id, automaticky nacitam content
        #----------------------------------------------------------------------
        if objPar is not None: self.contLoad(userId, objPar)

        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.init: Done")
        self.journal.O()
        
    #--------------------------------------------------------------------------
    def copy(self):
        "Creates copy of this Object"
        
        self.journal.M("{self.name}.copy:")
        
        copyObj = Object(self.journal, self.dms, self.userId, self.lang, self.classId)
        copyObj.contSet(contList=self.conts)
        
        return copyObj
    
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Object"
        
        return ''.join(self.info())

    #--------------------------------------------------------------------------
    def info(self, lvl=2):
        "Returns info about the Object"

        toRet = [f"{3*' '*lvl}{self.name}> ["]
        toRet.append('\n')
        
        for element in self.conts:
            
            if type(element)==dict: 
                toRet.append(f"{3*' '*(lvl+1)}{str(element)}")
                toRet.append('\n')
                
            else                  : toRet.extend(element.info(lvl+1))
            
            
        toRet.append(f"{3*' '*lvl}]")
        toRet.append('\n')

        return toRet

    #--------------------------------------------------------------------------
    def html(self):
        "This method should be overrided and return html code for this Object"

        self.journal.I("{self.name}.html:")
        toRet = ''
        
        #----------------------------------------------------------------------
        # Prejdem vsetky polozky v conts
        #----------------------------------------------------------------------
        for item in self.conts:
            
            #------------------------------------------------------------------
            # Ak je polozka typu Object
            #------------------------------------------------------------------
            if type(item)==dict: toRet += self.itemRender(item)
            else               : toRet += item.html()
        
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #==========================================================================
    # Praca s contentom objektu
    #--------------------------------------------------------------------------
#!!!! znacka
    def contLoad(self, who, objPar):
        """"Loads content of the object from Database as list [{item}, {item}, <Object>, {item}, ...] """
        
        self.journal.I(f"{self.name}.contLoad: For parent '{objPar}'")

        #----------------------------------------------------------------------
        # Inicializacia odpovede
        #----------------------------------------------------------------------
        self.conts = []
        
        #----------------------------------------------------------------------
        # Nacitanie zoznamu definicii vnorenych objektov
        #----------------------------------------------------------------------
        rows = self.readObjs(who, objPar)

        #----------------------------------------------------------------------
        # Prehladanie definicii vnorenych objektov pre parenta objPar
        #----------------------------------------------------------------------
        for row in rows:

            #------------------------------------------------------------------
            # Precitam definiciu vnoreneho objektu
            #------------------------------------------------------------------
            objId = row[1]
            self.journal.M(f"{self.name}.contLoad: '{objPar}.{objId}' is being analysed...")

            #------------------------------------------------------------------
            # Ak nie som sam sebe parentom
            #------------------------------------------------------------------
            if objId != objPar:
                
                #--------------------------------------------------------------
                # Na zaklade definicie vytvorim vnoreny Object a vlozim ho do conts
                #--------------------------------------------------------------
                subObj = Object(self.journal, self.dms, self.userId, self.lang, self.classId, objPar=objId)
                self.conts.append(subObj)

        #----------------------------------------------------------------------
        # Doplnim zoznam itemov parent objektu
        #----------------------------------------------------------------------
        items = self.resourceGet(who, objId=objPar)
                    
        if len(items) > 0: 
            
            self.conts.extend( items )
            self.journal.M(f"{self.name}.contLoad: '{objPar}' has resource {items}")
            
        else: self.journal.M(f"{self.name}.contLoad: '{objPar}' has no resource")

        #----------------------------------------------------------------------
        self.journal.O()
        return self.conts
    
    #--------------------------------------------------------------------------
    def contSet(self, who, contList):
        """"Sets content of the object  as list [{item}, {item}, <Object>, {item}, ...] """
        
        self.journal.I(f"{self.name}.contSet: '{contList}'")
        
        self.conts = contList

        #----------------------------------------------------------------------
        self.journal.O()
        return self.conts

    #--------------------------------------------------------------------------
    def contKeyVal(self, who, key):
        """"Returns value for the first occurence of the <key> in object's content"""
        
        self.journal.I(f"{self.name}.contKeyVal: Key = '{key}'")
        
        #----------------------------------------------------------------------
        # Prejdem vsetky polozky v conts
        #----------------------------------------------------------------------
        for element in self.conts:
            
            #------------------------------------------------------------------
            # Ak je to dictionary
            #------------------------------------------------------------------
            if type(element)==dict:
            
                #--------------------------------------------------------------
                # Ak sa v dict nachadza key
                #--------------------------------------------------------------
                if key in element.keys():
                
                    self.journal.O()
                    return element[key]

        #----------------------------------------------------------------------
        self.journal.I(f"{self.name}.contKeyVal: Key = '{key}' was not found", True)
        self.journal.O()
        return None

    #--------------------------------------------------------------------------
    def contCopy(self, who):
        """"Creates deep copy of the object's content"""
        
        self.journal.I(f"{self.name}.contCopy:")
        
        copyCont = []
        
        #----------------------------------------------------------------------
        # Prejdem vsetky polozky v conts
        #----------------------------------------------------------------------
        for element in self.conts:
            
            #------------------------------------------------------------------
            # Vytvorim kopiu polozky
            #------------------------------------------------------------------
            copyElement = self.copy()
            
            #------------------------------------------------------------------
            # Pridam kopiu do kopie contentu
            #------------------------------------------------------------------
            copyCont.append(copyElement)

        #----------------------------------------------------------------------
        self.journal.O()
        return copyCont

    #--------------------------------------------------------------------------
    def contSort(self, who, key):
        """"Sorts content [{item}, <obj>, {item}, ...] by respective key"""
        
        self.journal.I(f"{self.name}.contSort: Key = '{key}'")
 
        tupleLst = []
            
        #----------------------------------------------------------------------
        # Ziskam list tuples tupleLst = [(keyValue, obj)]
        #----------------------------------------------------------------------
        for element in self.conts:
            
            pos = None
            
            #------------------------------------------------------------------
            # Ak je to dictionary
            #------------------------------------------------------------------
            if type(element)==dict:
                if key in element.keys(): pos = element[key]
                                         
            #------------------------------------------------------------------
            # Ak je to Object
            #------------------------------------------------------------------
            else: 
                pos = element.contKeyVal(who, key=key)

            #------------------------------------------------------------------
            # Skontrolujem definiciu pozicie
            #------------------------------------------------------------------
            if pos is None:
                    
                self.journal.M(f"{self.name}.contSort: Element without key '{key}' will be skipped", True)
                continue

            else:
                tupleLst.append( (pos, element) )
                
        #----------------------------------------------------------------------
        # Zosortujem list podla Pos
        #----------------------------------------------------------------------
        tupleLst.sort( key=lambda tupl: tupl[0] )
        print(tupleLst)
            
        #----------------------------------------------------------------------
        # Prekodujem content podla sorted tupleLst
        #----------------------------------------------------------------------
        self.conts = []
            
        for tupl in tupleLst:
                
                self.conts.append(tupl[1])

        #----------------------------------------------------------------------
        self.journal.O()
        return self.conts

    #==========================================================================
    # Privatne metody
    #--------------------------------------------------------------------------
    def readObjs(self, who, objPar):
        "Reads and returns list of objects ownd by parent object <objPar>"
        
        self.journal.I(f"{self.name}.readObjs: For parent '{objPar}'")
        toRet = []
        
        #----------------------------------------------------------------------
        # Priprava podmienky pre citanie db
        #----------------------------------------------------------------------
        pagStr = gen.quoted(self.classId)
        parStr = gen.quoted(objPar)
 
        #----------------------------------------------------------------------
        # Ziskanie zoznamu objektov pre dany class a parent objekt
        #----------------------------------------------------------------------
        #              0         1          2         3        4            5            6      7
        cols = ('CLASS_ID', 'OBJ_ID', 'OBJ_PAR', 'C_FUNC', 'NOTES', 'D_CREATED', 'D_CHANGED', 'WHO')
        
        sql = f"""select {','.join(cols)} from {Config.tabObj} 
                  where 
                         CLASS_ID = {pagStr} 
                     and OBJ_PAR  = {parStr}
                     and C_FUNC   = 'A'
                     
                  order by OBJ_PAR, OBJ_ID"""
        
        rows = self.dms.readDb(who, sql)

        #----------------------------------------------------------------------
        # Kontrola existencie objektov
        #----------------------------------------------------------------------
        if type(rows)==int or len(rows)==0:
            
            self.journal.M(f"{self.name}.readObjs: Parent '{objPar}' has no children objects")
            self.journal.O()
            return toRet

        #----------------------------------------------------------------------
        objStr = ','.join([row[1] for row in rows])
        self.journal.M(f"{self.name}.readObjs: Parent '{objPar}' consits of objects [{objStr}]")
        
        #----------------------------------------------------------------------
        self.journal.O()
        return rows
        
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
            
            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'objectRegister()', 'NO_ACT', 'OK', 
                         stat="automatic object registration" )
        else:
            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'objectRegister()', 'NO_ACT', 'ER', 
                         stat="Object registration failed for pag/obj" )

        #----------------------------------------------------------------------
        self.journal.O()

    #==========================================================================
    # Praca s Resources (page-obj-resource-key)
    #--------------------------------------------------------------------------
    def resourceGet(self, who, objId):
        "Returns list of items for keys page-obj"
#!!!! znacka

        self.journal.I(f"{self.name}.resourceGet: '{self.classId}.{objId}'")
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
  
        rows = self.dms.readDb(who, sql)
        # self.journal.M(f"{self.name}.resourceGet: '{rows}'")
        
        #----------------------------------------------------------------------
        # Kontrola existencie resource
        #----------------------------------------------------------------------
        if type(rows)==int or len(rows)==0:
            
            self.journal.M(f"{self.name}.resourceGet: '{self.classId}.{objId}' no resource was found")
            self.journal.O()
            return toRet
    
        #----------------------------------------------------------------------
        # Vlozim udaje do struktury [ {item} ]
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
                # Ak je to novy itemId, vlozim predchadzajuci do zoznamu a resetnem item
                #--------------------------------------------------------------
                if prevItemId != itemId:
                    
                    if prevItemId != '': toRet.append(item)
                    
                    prevItemId = itemId
                    item = {}
                    
                #--------------------------------------------------------------
                # Akumulujem atributy aktualneho itemu
                #--------------------------------------------------------------
                item[key] = val

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
  
            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'resourceRegister()', 'OK', 
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
        if self.userId == 'SIQO':

            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'roleGet()', 'OK', 
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
  
        role = self.selectItem(self.userId, sql)

        #----------------------------------------------------------------------
        # Kontrola existencie role
        #----------------------------------------------------------------------
        if role is not None:

            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'roleGet()', 'OK', 
                         22, "user usr role for pag.obj is role" ) 
            self.journal.O()
            return role
    
        else:
            #------------------------------------------------------------------
            # User nema definovanu rolu. Zaregistrujem ho a vratim rolu
            #------------------------------------------------------------------
            role = self.roleRegister(who)

            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'roleGet()', 'OK', 
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
        if self.sSQL(self.userId, sql ) > 0:

            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'roleRegister()', 'OK', 
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
  
        role = self.selectItem(self.userId, sql)

        #----------------------------------------------------------------------
        # Kontrola existencie role
        #----------------------------------------------------------------------
        if role is not None:

            self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'roleAnonymGet()', 'NO_ACT', 'OK', stat="Anonymous role for pag.obj is role" )
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

        self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'roleSet()', 'OK', 
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

                self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'cacheSet()', 'ER', 3, 
                           "key is NOT setted to val" )  
                self.journal.O()
                return

        #----------------------------------------------------------------------
        self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'cacheSet()', 'OK', 
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

        self.sJournal(self.userId, 'NO_SESS', self.classId, self.name, 'cacheClear()', 'OK', 
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
    
    from   siqolib.journal       import SiqoJournal
    from   app_dms               import DMS
    
    journal = SiqoJournal('test-object', debug=8)
    dms     = DMS(journal, Config.dtbsName, Config.dtbsPath)
    
#    obj = Object(journal, dms, userId='palo4', lang='SK', classId='PagManHomepage', objPar='__HEAD__')
    obj = Object(journal, dms, userId='palo4', lang='SK', classId='PagManHomepage', objPar='__NAVB__')
    obj = Object(journal, dms, userId='palo4', lang='SK', classId='PagManHomepage', objPar='__STAG__')
    
    print(obj.conts)
    print()



    #print(obj.html())
    
    #rows = obj.readObjs('ja', objPar='__HEAD__')
    #rec = obj.objectGet('who', '__STAG__')


#==============================================================================
print(f"Object {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
