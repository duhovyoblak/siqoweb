#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os
from   datetime import datetime, timedelta

from werkzeug.security          import generate_password_hash, check_password_hash

import sqlite3
import siqo_lib.general   as gen
from   siqo_lib                 import SiqoJournal


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER          = 1.00
_CWD          = os.getcwd()
_TIME_WATCH   = 5            # Max duration in seconds without forced journal

if 'wsiqo-test-mode' in os.environ: _IS_TEST = True if os.environ['wsiqo-test-mode']=='1' else False 
else                              : _IS_TEST = False

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
    def __init__(self, journal, name):
        "Call constructor of Database and initialise it"
        
        journal.I(f"Database({name}).init:")

        self.journal       = journal
        self.name          = name
        self.con           = None
        self.cur           = None
        self.isOpen        = False
        self.prevCmd       = ''
        
        #----------------------------------------------------------------------
        # Connect to the database
        #----------------------------------------------------------------------
        self.open()

        #----------------------------------------------------------------------
        # Nacitanie json data pre page
        #----------------------------------------------------------------------
        self.journal.O(f"Database({self.name}).init")
        
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def open(self):

        self.con    = sqlite3.connect(f"{self.name}.db")
        self.cur    = self.con.cursor()
        self.isOpen = True
        

    #--------------------------------------------------------------------------
    def createDb(self):
        
        ddl     = gen.loadFile(self.journal, fileName=f"{self.name}.ddl", enc='utf-8')
        script  = gen.lines2str(ddl)
                
        self.cur.executescript(script)
        
        return script

    
    #==========================================================================
    # API for users
    #--------------------------------------------------------------------------
    def readDb(self, sql):

        self.journal.I(f'{self.name}.readDb: {sql}')

        #----------------------------------------------------------------------
        # Kontrola stavu konekcie
        #----------------------------------------------------------------------
        if not self.initialised:
            self.journal.M(f'{self.name}.readDb: ERROR : Connection is not initialised', True)
            self.journal.O('')
            return None
        
        #----------------------------------------------------------------------
        # Kontrola predchadzajuceho beziaceho prikazu
        #----------------------------------------------------------------------
        if self.prevCmd != '':
            self.journal.M(f'{self.name}.readDb: ERROR   : Previous command is still runnig', True)
            self.journal.M(f'{self.name}.readDb: prev SQL: {self.prevCmd}',                   True)
            self.journal.M(f'{self.name}.readDb: SQL     : {sql}',                             True)
            self.journal.O('')
            return None
        
        #----------------------------------------------------------------------
        # Citanie udajov z konekcie
        #----------------------------------------------------------------------
        try:
            bef = datetime.now()
            self.prevCmd = sql
            
            self.conn['cur'].execute(sql)
            rows = self.conn['cur'].fetchall()
            cnt  = len(rows)
            self.prevCmd = ''
            
            #------------------------------------------------------------------
            # Kontrola dlzky trvania prikazu
            #------------------------------------------------------------------
            aft = datetime.now()
            sec = (aft-bef).seconds
            if sec > _TIME_WATCH: self.journal.M('{}.readDb: {:8n} rows in {:4.0f} sec for {}'.format(self.name, cnt, sec, sql[:100].replace("\n"," ") ), True)

            #------------------------------------------------------------------
            self.journal.O('')
            return rows

        except Exception as err:
            self.journal.M(f'{self.name}.readDb: ERROR :{str(err)}', True)
            self.journal.M(f'{self.name}.readDb: SQL   :{sql}',      True)
            self.journal.O('')
            return None

    #--------------------------------------------------------------------------
    def sSql(self, sql, param='', log='B', logSql='Y', thread='', adat=0):

        self.journal.I(f"{self.name}.sSql: '{sql}' with param '{param}'")

        #----------------------------------------------------------------------
        # Kontrola stavu konekcie
        #----------------------------------------------------------------------
        if not self.initialised:
            self.journal.M(f'{self.name}.sSql: ERROR : Connection is not initialised', True)
            self.journal.M(f'{self.name}.sSql: SQL   : {sql}',                         True)
            self.journal.O('')
            return -1
        
        #----------------------------------------------------------------------
        # Kontrola predchadzajuceho nekomitovaneho prikazu
        #----------------------------------------------------------------------
        if self.prevCmd != '':
            self.journal.M(f'{self.name}.sSql: ERROR   : Previous command is not yet committed', True)
            self.journal.M(f'{self.name}.sSql: prev SQL: {self.prevCmd}',                        True)
            self.journal.M(f'{self.name}.sSql: SQL     : {sql}',                                 True)
            self.journal.O('')
            
            if log=='B':
                self.addMeta(act='M2', who=self.name, obj=f'SSQL {_VER}', res='ER', dsc= 'Previous command is not yet committed', thread=thread, adat=adat)
            return -1
        
        #----------------------------------------------------------------------
        # Zapis sql statementu do logu
        #----------------------------------------------------------------------
        if logSql=='Y':
            self.journal.M(f'{self.name}.sSql: SQL statement was logged in LogSQL table')

        #----------------------------------------------------------------------
        # Pokusim sa vykonat SQL prikaz
        #----------------------------------------------------------------------
        try:
            bef = datetime.now()
            self.prevCmd = sql
            
            if param != '': self.conn['cur'].execute(sql, param)
            else          : self.conn['cur'].execute(sql)
            
            cnt = self.conn['cur'].rowcount
            self.commitConn()  # Tu sa resetuje self.prevCmd

            #------------------------------------------------------------------
            # Kontrola dlzky trvania prikazu
            #------------------------------------------------------------------
            aft = datetime.now()
            sec = (aft-bef).seconds
            if sec > _TIME_WATCH: self.journal.M('{}.sSql: {:8n} rows in {:4.0f} sec for {}'.format(self.name, cnt, sec, sql[:100].replace("\n"," ") ), True)
                
            self.journal.O('')
            return cnt

        #----------------------------------------------------------------------
        # Error handling
        #----------------------------------------------------------------------
        except Exception as err:
            self.journal.M(f'{self.name}.sSql {_VER}: ERROR :{str(err)}', True)
            self.journal.M(f'{self.name}.sSql {_VER}: SQL   :{sql}',      True)
            self.journal.M(f'{self.name}.sSql {_VER}: PARAM :{param}',    True)

            #------------------------------------------------------------------
            if log=='B':
                try:
                    self.addMeta(act='M2', who=self.name, obj=f'SSQL {_VER}', res='ER', dsc=sql     , thread=thread, adat=adat)
                    self.addMeta(act='M2', who=self.name, obj=f'SSQL {_VER}', res='ER', dsc=str(err), thread=thread, adat=adat)
                    
                except Exception as errB:
                    self.journal.M(f'{self.name}.sSql: DEEP ERROR :{str(errB)}', True)
                    self.journal.M(f'{self.name}.sSql: DEEP SQL   :{sql}',       True)
                    self.journal.M(f'{self.name}.sSql: DEEP PARAM :{param}',     True)

            #------------------------------------------------------------------
            self.journal.O('')
            return -1

    #--------------------------------------------------------------------------
    def sSqlMany(self, sql, data, batch=100000):

        ld = len(data)
        self.journal.I(f'{self.name}.sSqlMany: {sql} for data length {ld} via batch {batch}')

        #----------------------------------------------------------------------
        # Kontrola stavu konekcie
        #----------------------------------------------------------------------
        if not self.initialised:
            self.journal.M(f'{self.name}.sSqlMany: ERROR : Connection is not initialised', True)
            self.journal.M(f'{self.name}.sSqlMany: SQL   : {sql}',                         True)
            self.journal.O('')
            return -1
        
        #----------------------------------------------------------------------
        # Kontrola predchadzajuceho nekomitovaneho prikazu
        #----------------------------------------------------------------------
        if self.prevCmd != '':
            self.journal.M(f'{self.name}.sSqlMany: ERROR   : Previous command is not yet committed', True)
            self.journal.M(f'{self.name}.sSqlMany: prev SQL: {self.prevCmd}',                        True)
            self.journal.M(f'{self.name}.sSqlMany: SQL     : {sql}',                                 True)
            self.journal.O('')
            return -1
        
        #----------------------------------------------------------------------
        # Kontrola existencie udajov
        #----------------------------------------------------------------------
        if ld==0:
            self.journal.M(f'{self.name}.sSqlMany: ERROR {sql} has empty data', True)
            self.journal.O('')
            return -1

        #----------------------------------------------------------------------
        self.journal.M('1st row: {}'.format(data[0]))

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
                self.conn['cur'].executemany(sql, data[a:b])
                cnt += self.conn['cur'].rowcount
                self.commitConn()   # Tu sa resetuje self.prevCmd

                self.journal.M(f'{self.name}.sSqlMany: batch from {a} till {b} done')
                a = b

        except Exception as err:
            self.journal.M(f'{self.name}.sSqlMany: ERROR  :{str(err)}', True)
            self.journal.M(f'{self.name}.sSqlMany: SQL    :{sql}',      True)
            self.journal.M(f"{self.name}.sSqlMany: DATA[a]:{data[a]}",  True)
            self.journal.M(f'{self.name}.sSqlMany: DATA INTERVAL <{a}, {b}>', True)
            self.journal.O('')
            return -1

        #----------------------------------------------------------------------
        aft = datetime.now()
        sec = (aft-bef).seconds

        if sec > _TIME_WATCH: self.journal.M('{}.sSqlMany: {:8n} rows in {:4.0f} sec for {}'.format(self.name, cnt, sec, sql[:100].replace("\n"," ")), True)
        self.journal.O('')
        return cnt




#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    journal = SiqoJournal('test-db', debug=5)
    db = Database(journal, "test")
    db.createDb()

#==============================================================================
print(f"Database {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
