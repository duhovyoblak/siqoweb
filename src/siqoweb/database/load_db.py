# Loads pagman.db and stores it in 'db', an instance of Database()

from siqoweb.database import Database
from   siqolib.journal import SiqoJournal
journal = SiqoJournal('test-db', debug=5)
from   config import Config
db = Database(journal, Config.dtbsName, Config.dtbsPath, autoInit=False)
