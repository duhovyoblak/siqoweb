#==============================================================================
#  SIQO Homepage: DMS API
#------------------------------------------------------------------------------
import os

import siqo_lib.general   as gen

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER       = 1.00
_PATH      = '../DMS/'
_DMS_TABLE = 'PM_DMS'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# package's tools
#------------------------------------------------------------------------------

#==============================================================================
# 
#------------------------------------------------------------------------------
def loadJson(fName):
    
    journal.I(f"loadJson: {fName}")
    
    toRet = gen.loadJson(journal, fileName = f"{_PATH}{fName}")
    
    journal.O()
    return toRet

#==============================================================================
# Class DMS
#------------------------------------------------------------------------------
class DMS:
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, db):
        "Call constructor of DMS"

        journal.I("DMS.init:")
        
        #----------------------------------------------------------------------
        # Identifikacia objektu
        #----------------------------------------------------------------------
        self.name    = "DMS"
        self.journal = journal
        self.db      = db        # Database with DMS metadata
        self.docs    = []        # List of documents in RAM
        
        #----------------------------------------------------------------------
        self.journal.O()
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this DMS"
        
        return f"DMS>{' '.join(self.info())}"

    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the DMS"

        toRet = []

        return toRet

    #==========================================================================
    # Praca s jednym dokumentom
    #--------------------------------------------------------------------------
    def docById(self, who, idx):
        
        self.journal.I(f"{self.name}.docById: ID = '{id}'")
        
        doc = self.docRead(who, where = f"DOC_ID = {idx}")
        
        self.journal.O()
        return doc


    #==========================================================================
    # Privatne metody
    #--------------------------------------------------------------------------
    def docRead(self, who, where='1=1'):

        self.journal.I(f"{self.name}.docRead: where '{where}'")
        
        self.docs = self.db.readTable(who, _DMS_TABLE, where)

        # DOC_ID,C_FUNC,USER_ID,D_CREATED,C_TYPE,FILENAME,ORIGNAME,THUMBNAME,
        # N_SIZE,C_PUB,TITLE,NOTES,D_VALID,D_EXPIRY,MD5
        
        #----------------------------------------------------------------------
        self.journal.O(f"{self.name}.docRead: {len(self.docs)} documents was read")
        
        return self.docs

    #==========================================================================
    # Praca s Resources (page-obj-resource-key)
    #--------------------------------------------------------------------------

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqo_lib                 import SiqoJournal
    journal = SiqoJournal('test-DMS', debug=4)
    
    from   siqo_web.config          import Config
    from   siqo_web.database        import Database
    db = Database(journal, Config.dtbsName, Config.dtbsPath, autoInit=False)
    
    dms = DMS(journal, db)
    
    docs = dms.docRead('ja')
    doc  = dms.docById('ja', 57)

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"dms {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
