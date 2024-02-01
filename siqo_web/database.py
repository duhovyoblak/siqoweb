#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os
import re
from   datetime                 import datetime, timedelta

import sqlite3
import siqo_lib.general         as gen
from   siqo_lib                 import SiqoJournal

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER       = 1.00
_CWD       = os.getcwd()

_PING_LAG  =    2    # Number of hours after which ping is recomended
_SQL_WATCH =   10    # Max duration of SQL in seconds without forced journal
_SQL_BATCH = 1000    # Default data batch for 
_SQL_SMPL  =  100    # Max first chars from SQL statement for print into journal

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Class Database
#------------------------------------------------------------------------------
class Database:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dtbs, path=''):
        "Call constructor of Database and initialise it"
        
        journal.I(f"Database({dtbs}).init:")

        self.journal       = journal
        self.path          = path
        self.dtbs          = dtbs
        
        self.con           = None
        self.cur           = None
        self.isOpen        = False
        self.lastPing      = None
        
        self.prevCmd       = ''

        #----------------------------------------------------------------------
        # Connect to the database
        #----------------------------------------------------------------------
        self.openDb()

        #----------------------------------------------------------------------
        # Nacitanie json data pre page
        #----------------------------------------------------------------------
        self.journal.O(f"Database({self.dtbs}).init")
        
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def openDb(self):

        self.journal.I(f"{self.dtbs}.:openDb")

        self.con      = sqlite3.connect(f"{self.path}{self.dtbs}.db")
        self.cur      = self.con.cursor()
        self.isOpen   = True
        self.lastPing = datetime.now(gen._TIME_ZONE)
        
        self.journal.O()

    #--------------------------------------------------------------------------
    def closeDb(self):
        "Close opened session/connection to RDBMS"

        self.journal.I(f"{self.dtbs}.:closeDb")

        self.commit()
        if self.cur is not None: self.cur.close()

        self.journal.O()

    #==========================================================================
    # DB tools
    #--------------------------------------------------------------------------
    def commit(self):
        "Commits open transaction"

        if self.con is not None: self.con.commit()
        self.journal.M(f'{self.dtbs}.commit: Commit {self.prevCmd}')

        self.prevCmd = ''

    #--------------------------------------------------------------------------
    def rollback(self):
        "Rollbacks open transaction"

        if self.con is not None: self.con.rollback()
        self.journal.M(f'{self.dtbs}.rollback: Rollback {self.prevCmd}')

        self.prevCmd = ''

    #--------------------------------------------------------------------------
    def tables(self):
        "Returns list of tables in the database"

        self.journal.I(f'{self.dtbs}.tables:')
        toRet = []
        
        #----------------------------------------------------------------------
        # Ziskam zoznam tabuliek
        #----------------------------------------------------------------------
        rows = self.readDb(f"{self.dtbs}", sql="SELECT name FROM sqlite_master WHERE type='table' order by name")
        
        if type(rows) == int:
            self.journal.M(f'{self.dtbs}.tables: Method failed', True)
            self.journal.O()
            return toRet
        
        #----------------------------------------------------------------------
        # Skonvertujem do listu
        #----------------------------------------------------------------------
        toRet = [row[0] for row in rows]

        self.journal.M(f'{self.dtbs}.tables: {toRet}')
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def attributes(self, table):
        "Returns list of attributes for respective table"

        self.journal.I(f"{self.dtbs}.attributes: table = '{table}'")
        toRet = []
        
        #----------------------------------------------------------------------
        # Ziskam zoznam tabuliek
        #----------------------------------------------------------------------
        rows = self.readDb( f"{self.dtbs}", 
                           sql="SELECT sql FROM sqlite_master WHERE type='table' and name=?",
                           params=(table,))
        
        if type(rows) == int:
            self.journal.M(f'{self.dtbs}.attributes: Method failed', True)
            self.journal.O()
            return toRet
        
        #----------------------------------------------------------------------
        # Ziskam text DDL prikazu CREATE TABLE ( content )
        #----------------------------------------------------------------------
        sql = rows[0][0].replace('\n', ' ')
        
        #----------------------------------------------------------------------
        # Vystrihnem content
        #----------------------------------------------------------------------
        cont = re.findall(r'\(.*\)', sql)[0][1:-1]
        
        #----------------------------------------------------------------------
        # Odstranim poznamky /*...*/ a ziskam cisty content
        #----------------------------------------------------------------------
        clear = re.sub(r'\/\*.*?\*\/', '', cont)

        #----------------------------------------------------------------------
        # Skonvertujem do listu
        #----------------------------------------------------------------------
        lst = clear.split(',')

        #----------------------------------------------------------------------
        # Extrahujem atributy do vysledneho listu
        #----------------------------------------------------------------------
        for line in lst:

            attr = line.strip().split(' ')[0]
            if attr not in ['PRIMARY', 'FOREIGN']: toRet.append(attr)

        #----------------------------------------------------------------------
        self.journal.M(f'{self.dtbs}.attributes: {toRet}')
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def views(self):
        "Returns list of views in the database"

        self.journal.I(f'{self.dtbs}.views:')
        toRet = []

        #----------------------------------------------------------------------
        # Ziskam zoznam views
        #----------------------------------------------------------------------
        rows = self.readDb(f"{self.dtbs}", sql="SELECT name FROM sqlite_master WHERE type='view' order by name")

        if type(rows) == int:
            self.journal.M(f'{self.dtbs}.views: Method failed', True)
            self.journal.O()
            return toRet
        
        #----------------------------------------------------------------------
        # Skonvertujem do listu
        #----------------------------------------------------------------------
        toRet = [row[0] for row in rows]

        self.journal.M(f'{self.dtbs}.views: {toRet}')
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def indexes(self, table=''):
        "Returns list of indexes in the database or in the table"

        self.journal.I(f"{self.dtbs}.indexes: table = '{table}'")
        toRet = {}
        
        #----------------------------------------------------------------------
        # Ziskam zoznam indexov v DB alebo pre jednu tabulku
        #----------------------------------------------------------------------
        where  = ""
        params = None
        
        if table != '': 
            where  = " and tbl_name = ?"
            params = (table,)
        
        rows = self.readDb(f"{self.dtbs}", 
                            sql = f"SELECT tbl_name, name FROM sqlite_master WHERE type='index' {where} order by tbl_name, name",
                            params = params)
        
        if type(rows) == int:
            self.journal.M(f'{self.dtbs}.indexes: Method failed', True)
            self.journal.O()
            return toRet
        
        #----------------------------------------------------------------------
        # Skonvertujem do dict
        #----------------------------------------------------------------------
        for row in rows:
            
            if row[0] not in toRet.keys(): toRet[row[0]] = []
            toRet[row[0]].append(row[1])
            
        self.journal.M(f'{self.dtbs}.indexes: {toRet}')
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def ping(self, force=False):
        "Pings this connection. Returns true if succeed"

        self.journal.I(f'{self.dtbs}.ping: Force = {force}')

        now = datetime.now(gen._TIME_ZONE)

        #----------------------------------------------------------------------
        # Ak je ping vynuteny alebo uz uplynulo vela casu
        #----------------------------------------------------------------------
        if force or ( now-self.lastPing > timedelta(hours=_PING_LAG) ):

            test = self.readDb(self.dtbs, "select 'OK'")
                
            if (test is not None) and (type(test)==list):
                self.lastPing = datetime.now(gen._TIME_ZONE)
                self.journal.M(f"{self.dtbs}.ping: Connection was pinged")

            else:
                self.isOpen = False
                self.journal.M(f"{self.dtbs}.ping: Ping failed", True)

        #----------------------------------------------------------------------
        self.journal.O()
        return self.isOpen

    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def toJson(self, table, where='1=1'):
        
        self.journal.I(f"{self.dtbs}.toJson: table ={table} where {where}")
        toRet = []
        
        #----------------------------------------------------------------------
        # Ziskam zoznam atributov
        #----------------------------------------------------------------------
        atts = self.attributes(table)

        #----------------------------------------------------------------------
        # Nacitam riadky na konverziu do json
        #----------------------------------------------------------------------
        sql  = f"select * from {table} where {where}"
        rows = self.readDb(self.dtbs, sql)
        
        #----------------------------------------------------------------------
        # Konverzia do json
        #----------------------------------------------------------------------
        toRet.append(atts)
        
        for row in rows:
            toRet.append(list(row))
        
        self.journal.O()
        return toRet

    #==========================================================================
    # Backup&Restore
    #--------------------------------------------------------------------------
    def backup(self):
        
        pass

    #--------------------------------------------------------------------------
    def restore(self, fName):
        
        pass
        
        
        
    #==========================================================================
    # Work with DB
    #--------------------------------------------------------------------------
    def createDb(self, who):
        
        self.journal.I(f"{who}@{self.dtbs}.:createDb from path='{self.path}'")

        self.sSqlScript(who, fName=f"{self.dtbs}.ddl" )
        
        self.journal.O()

    #--------------------------------------------------------------------------
    def readDb(self, who, sql, params = None):

        self.journal.I(f'{who}@{self.dtbs}.readDb: {sql}')

        #----------------------------------------------------------------------
        # Kontrola stavu konekcie
        #----------------------------------------------------------------------
        if not self.isOpen:
            self.journal.M(f'{who}@{self.dtbs}.readDb: ERROR : Connection is not open', True)
            self.journal.O('')
            return -1
        
        #----------------------------------------------------------------------
        # Kontrola predchadzajuceho beziaceho prikazu
        #----------------------------------------------------------------------
        if self.prevCmd != '':
            self.journal.M(f'{who}@{self.dtbs}.readDb: ERROR   : Previous command is still runnig', True)
            self.journal.M(f'{who}@{self.dtbs}.readDb: prev SQL: {self.prevCmd}',                   True)
            self.journal.M(f'{who}@{self.dtbs}.readDb: SQL     : {sql}',                            True)
            self.journal.O('')
            return -2
        
        #----------------------------------------------------------------------
        # Citanie udajov z konekcie
        #----------------------------------------------------------------------
        try:
            bef = datetime.now()
            self.prevCmd = sql
            
            if params is None: res  = self.cur.execute(sql)
            else             : res  = self.cur.execute(sql, params)
            
            rows = res.fetchall()
            cnt  = len(rows)
            self.prevCmd = ''
            
            #------------------------------------------------------------------
            # Kontrola dlzky trvania prikazu
            #------------------------------------------------------------------
            aft = datetime.now()
            sec = (aft-bef).seconds
            if sec > _SQL_WATCH: self.journal.M(f"{who}@{self.dtbs}.readDb: {cnt:8n} rows in {sec:4.0f}", True)

            #------------------------------------------------------------------
            self.journal.O('')
            return rows

        except Exception as err:

            self.prevCmd = ''

            self.journal.M(f'{who}@{self.dtbs}.readDb: ERROR :{str(err)}', True)
            self.journal.M(f'{who}@{self.dtbs}.readDb: SQL   :{sql}',      True)
            self.journal.O('')
            return -3

    #--------------------------------------------------------------------------
    def sSql(self, who, sql, param=''):

        self.journal.I(f"{who}@{self.dtbs}.sSql: '{sql}' with param '{param}'")

        #----------------------------------------------------------------------
        # Kontrola stavu konekcie
        #----------------------------------------------------------------------
        if not self.isOpen:
            self.journal.M(f'{who}@{self.dtbs}.sSql: ERROR : Connection is not open', True)
            self.journal.O('')
            return -1
        
        #----------------------------------------------------------------------
        # Kontrola predchadzajuceho nekomitovaneho prikazu
        #----------------------------------------------------------------------
        if self.prevCmd != '':
            self.journal.M(f'{who}@{self.dtbs}.sSql: ERROR   : Previous command is not yet committed', True)
            self.journal.M(f'{who}@{self.dtbs}.sSql: prev SQL: {self.prevCmd}',                        True)
            self.journal.M(f'{who}@{self.dtbs}.sSql: SQL     : {sql}',                                 True)
            self.journal.O('')
            return -2
            
        #----------------------------------------------------------------------
        # Pokusim sa vykonat SQL prikaz
        #----------------------------------------------------------------------
        try:
            bef = datetime.now()
            self.prevCmd = sql
            
            if param != '': self.cur.execute(sql, param)
            else          : self.cur.execute(sql)
            
            cnt = self.cur.rowcount
            self.commit()  # Tu sa resetuje self.prevCmd

            #------------------------------------------------------------------
            # Kontrola dlzky trvania prikazu
            #------------------------------------------------------------------
            aft = datetime.now()
            sec = (aft-bef).seconds
            mes = sql[:_SQL_SMPL].replace('\n',' ')
            if sec > _SQL_WATCH: self.journal.M(f"{who}@{self.dtbs}.sSql: {cnt:8n} rows in {sec:4.0f} sec for {mes}", True)
                
            self.journal.O('')
            return cnt

        #----------------------------------------------------------------------
        # Error handling
        #----------------------------------------------------------------------
        except Exception as err:
            
            self.rollback()
            
            self.journal.M(f'{who}@{self.dtbs}.sSql {_VER}: ERROR :{str(err)}', True)
            self.journal.M(f'{who}@{self.dtbs}.sSql {_VER}: SQL   :{sql}',      True)
            self.journal.M(f'{who}@{self.dtbs}.sSql {_VER}: PARAM :{param}',    True)

            self.journal.O('')
            return -3

    #--------------------------------------------------------------------------
    def sSqlMany(self, who, sql, data, batch=_SQL_BATCH):

        ld = len(data)
        self.journal.I(f'{who}@{self.dtbs}.sSqlMany: {sql} for data length {ld} via batch {batch}')

        #----------------------------------------------------------------------
        # Kontrola stavu konekcie
        #----------------------------------------------------------------------
        if not self.isOpen:
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: ERROR : Connection is not open', True)
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: SQL   : {sql}',                  True)
            self.journal.O('')
            return -1
        
        #----------------------------------------------------------------------
        # Kontrola predchadzajuceho nekomitovaneho prikazu
        #----------------------------------------------------------------------
        if self.prevCmd != '':
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: ERROR   : Previous command is not yet committed', True)
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: prev SQL: {self.prevCmd}',                        True)
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: SQL     : {sql}',                                 True)
            self.journal.O('')
            return -2
        
        #----------------------------------------------------------------------
        # Kontrola existencie udajov
        #----------------------------------------------------------------------
        if ld==0:
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: ERROR {sql} has empty data', True)
            self.journal.O('')
            return -3

        #----------------------------------------------------------------------
        self.journal.M(f"1st row: {data[0]}")

        cnt = 0
        a   = 0
        bef = datetime.now()

        #----------------------------------------------------------------------
        # Pokusim sa vykonat SQL prikaz
        #----------------------------------------------------------------------
        try:
            while a < ld:

                b = a + batch
                if b > ld: b=ld

                self.prevCmd = sql
                self.cur.executemany(sql, data[a:b])
                cnt += self.cur.rowcount
                self.commit()                     # Tu sa resetuje self.prevCmd

                self.journal.M(f'{self.dtbs}.sSqlMany: batch from {a} till {b} done')
                a = b

        except Exception as err:
            
            self.rollback()
            
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: ERROR  :{str(err)}', True)
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: SQL    :{sql}',      True)
            self.journal.M(f"{who}@{self.dtbs}.sSqlMany: DATA[a]:{data[a]}",  True)
            self.journal.M(f'{who}@{self.dtbs}.sSqlMany: DATA INTERVAL <{a}, {b}>', True)
            self.journal.O('')
            return -4

        #----------------------------------------------------------------------
        aft = datetime.now()
        sec = (aft-bef).seconds
        mes = sql[:_SQL_SMPL].replace('\n',' ')

        if sec > _SQL_WATCH: self.journal.M(f"{who}@{self.dtbs}.sSqlMany: {cnt:8n} rows in {sec:4.0f} sec for {mes}", True)
        self.journal.O('')
        return cnt

    #--------------------------------------------------------------------------
    def sSqlScript(self, who, fName, path=None):

        self.journal.I(f"{who}@{self.dtbs}.sSqlScript: '{fName}'")

        #----------------------------------------------------------------------
        # Kontrola stavu konekcie
        #----------------------------------------------------------------------
        if not self.isOpen:
            self.journal.M(f'{who}@{self.dtbs}.sSqlScript: ERROR : Connection is not open', True)
            self.journal.O('')
            return -1
        
        #----------------------------------------------------------------------
        # Kontrola predchadzajuceho nekomitovaneho prikazu
        #----------------------------------------------------------------------
        if self.prevCmd != '':
            self.journal.M(f'{who}@{self.dtbs}.sSqlScript: ERROR   : Previous command is not yet committed', True)
            self.journal.M(f'{who}@{self.dtbs}.sSqlScript: prev SQL: {self.prevCmd}',                        True)
            self.journal.O('')
            return -2
            
        #----------------------------------------------------------------------
        # Kontrola a ziskanie skriptu
        #----------------------------------------------------------------------
        if path is None: fName = f"{self.path}{fName}"
        else           : fName = f"{path}{fName}"

        lines  = gen.loadFile(self.journal, fileName=fName, enc='utf-8')
        if len(lines) == 0:
            self.journal.M(f'{who}@{self.dtbs}.sSqlScript: ERROR   : Script is empty or does not exist', True)
            self.journal.O('')
            return -3
        
        script = gen.lines2str(lines)

        #----------------------------------------------------------------------
        # Pokusim sa vykonat SQL prikaz
        #----------------------------------------------------------------------
        try:
            bef = datetime.now()
            self.prevCmd = f"script '{fName}'"
            
            self.cur.executescript(script)
            
            cnt = self.cur.rowcount
            self.commit()  # Tu sa resetuje self.prevCmd

            #------------------------------------------------------------------
            # Kontrola dlzky trvania prikazu
            #------------------------------------------------------------------
            aft = datetime.now()
            sec = (aft-bef).seconds
            mes = fName
            if sec > _SQL_WATCH: self.journal.M(f"{who}@{self.dtbs}.sSqlScript: {cnt:8n} rows in {sec:4.0f} sec for {mes}", True)
                
            self.journal.O('')
            return cnt

        #----------------------------------------------------------------------
        # Error handling
        #----------------------------------------------------------------------
        except Exception as err:
            
            self.rollback()
            
            self.journal.M(f"{who}@{self.dtbs}.sSqlScript: ERROR :'{str(err)}'", True)
            self.journal.M(f"{who}@{self.dtbs}.sSqlScript: '{fName}'",           True)
            self.journal.M(f"{who}@{self.dtbs}.sSqlScript: '{script}'",          True)
            self.journal.O('')
            return -4

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    journal = SiqoJournal('test-db', debug=5)

    db = Database(journal, "test")

    db.createDb(who="who")
    db.sSqlScript('who', fName='test.ini')
 
    tables     = db.tables()
    attributes = db.attributes('SUSER')
    views      = db.views()
    indexes    = db.indexes()
    indexes    = db.indexes('SUSER')
    
#==============================================================================
print(f"Database {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------