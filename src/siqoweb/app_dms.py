#==============================================================================
#  SIQO Homepage: DMS API
#------------------------------------------------------------------------------
import os

from   flask                    import Flask, url_for, render_template, make_response

import siqolib.general         as gen
from   config          import Config

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER       = '1.01'

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
    # Tools
    #--------------------------------------------------------------------------
    def uri(self, fName):
        
        return f"{Config.dmsPath}{fName}"

    #==========================================================================
    # Praca s jednym dokumentom
    #--------------------------------------------------------------------------
    def docById(self, who, idx):
        
        self.journal.I(f"{self.name}.docById: ID = '{id}'")
        
        doc = self.docRead(who, where = f"DOC_ID = {idx}")[0]
        doc['URI'] = url_for('static', filename=f"dms/{doc['FILENAME']}")
        
        self.journal.O()
        return doc


    #==========================================================================
    # Privatne metody
    #--------------------------------------------------------------------------
    def docRead(self, who, where='1=1'):

        self.journal.I(f"{self.name}.docRead: where '{where}'")
        
        self.docs = self.db.readTable(who, Config.tabDms, where)

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
    
    from   siqo_web.database        import Database
    db = Database(journal, Config.dtbsName, Config.dtbsPath, autoInit=False)
    
    dms = DMS(journal, db)
    
    docs = dms.docRead('ja')
#    doc  = dms.docById('ja', 57)

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"app_dms {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
