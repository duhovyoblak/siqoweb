#==============================================================================
#  SIQO Homepage: DMS API
#------------------------------------------------------------------------------
import os
from   flask                 import url_for

import siqolib.general       as gen
from   config                import Config
from   database              import Database

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.06'

_DMS_PREFIX    = 'SF'
_DAY_CHANGES   = 32       # Pocet dni, pocas ktorych sa item povazuje za cerstvo zmeneny
_TITLE_MAX     = 36       # Maximalny pocet zobrazenych znakov TITLE v selectore

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
class DMS(Database):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, dtbs, path):
        "Call constructor of DMS"

        journal.I("DMS.init:")
        
        #----------------------------------------------------------------------
        # Inicializacia databazy
        #----------------------------------------------------------------------
        super().__init__(journal, dtbs, path)

        #----------------------------------------------------------------------
        # Identifikacia objektu
        #----------------------------------------------------------------------
        self.name    = f"DMS({dtbs})"
        self.journal = journal
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
    def idx2Fname(self, idx):
        
        return f"{Config.dmsPrefix}{str(idx).rjust(Config.dmsFnLen)}"

    #--------------------------------------------------------------------------
    def uri(self, fName):
        
        try: 
            return url_for('static', filename = f"{Config.dmsFolder}/{fName}")
        
        except RuntimeError as err:
            self.journal.M(f"{self.name}.uri: fName = '{fName}' ERROR", True)
            self.journal.M(f"{self.name}.uri: {str(err)}", True)
            return fName
            

    #==========================================================================
    # Praca s jednym dokumentom
    #--------------------------------------------------------------------------
    def docById(self, who, idx):
        
        self.journal.I(f"{self.name}.docById: IDX = '{idx}'")
        
        rows = self.docRead(who, where = f"DOC_ID = {idx}")
        
        if rows is None:
            self.journal.M(f'{self.name}.docById: Method failed', True)
            self.journal.O()
            return None
        
        if len(rows) < 1:
            self.journal.M(f'{self.name}.docById: Document with idx = {idx} does not exist', True)
            self.journal.O()
            return None
        
        if len(rows) > 1:
            self.journal.M(f'{self.name}.docById: Too many documents with idx = {idx}', True)
            self.journal.O()
            return None
        
        doc = rows[0]
        doc['URI'] = self.uri( doc['FILENAME'] )
        
        self.journal.O()
        return doc


    #==========================================================================
    # Privatne metody
    #--------------------------------------------------------------------------
    def docRead(self, who, where='1=1'):

        self.journal.I(f"{self.name}.docRead: where '{where}'")
        
        self.docs = self.readTable(who, Config.tabDms, where, header='detail')

        # DOC_ID,C_FUNC,USER_ID,D_CREATED,C_TYPE,FILENAME,ORIGNAME,THUMBNAME,
        # N_SIZE,C_PUB,TITLE,NOTES,D_VALID,D_EXPIRY,MD5
        
        #----------------------------------------------------------------------
        self.journal.O(f"{self.name}.docRead: {len(self.docs)} documents was read")
        
        return self.docs

    #==========================================================================
    # Praca s FORUM
    #--------------------------------------------------------------------------
    def loadForumItem(self, who, forumId, idx=0, target=''):
    
        self.journal.I(f"{self.name}.loadForumItem: {forumId}.{idx}")

        #----------------------------------------------------------------------
        # Ak NIE je zname idx nacitam root item fora, inak nacitam nacitam item
        #----------------------------------------------------------------------
        if idx > 0: where = f" FORUM_ID = '{forumId}' and ITEM_ID   = {idx}"
        else      : where = f" FORUM_ID = '{forumId}' and PARENT_ID = 0"

        self.journal.M(f"{self.name}.loadForumItem: {where}")
        
        #----------------------------------------------------------------------
        # Nacitanie polozky z DB ako dict
        #----------------------------------------------------------------------
        rows = self.readTable(who=who, table=Config.tabForum, where=where, header='detail')
        
        #----------------------------------------------------------------------
        # Kontrola existencie forum itemu
        #----------------------------------------------------------------------
        if len(rows) == 0: 

            self.journal.M(f"{self.name}.loadForumItem: Item {where} does not exist")
            self.journal.O()
            return (None, None)
        
        #----------------------------------------------------------------------
        # Konverzia dat do objektu
        #----------------------------------------------------------------------
        item = {}
        data = rows[0]

        if data is not None: 
            
            title = data['TITLE']
            if data['C_FUNC'] == 'K': title = f"KONCEPT: {title}"
            
            item['ITEM_ID'  ] = {'SK': data['ITEM_ID'  ], 'TYPE':'VAR'                        }
            item['PARENT_ID'] = {'SK': data['PARENT_ID'], 'TYPE':'VAR'                        }
            item['TITLE'    ] = {'SK': title,             'TYPE':'H2'                         }
            item['NARR'     ] = {'SK': data['NARRATOR' ], 'TYPE':'H3'                         }
            item['D_CRT'    ] = {'SK': data['D_CREATED'], 'TYPE':'DATE'                       }
            item['D_CHG'    ] = {'SK': data['D_CHANGED'], 'TYPE':'DATE'                       }
            item['TEXT'     ] = {'SK': data['ITEM'     ], 'TYPE':'TEXT_ITEM', 'target':target }

        else: 
            apology = f"Oops, it seems forum item {self.idx} doesn't exist in forum {self.target}"
            
            item['ITEM_ID'  ] = {'SK': -1               , 'TYPE':'VAR'   }
            item['PARENT_ID'] = {'SK': -1               , 'TYPE':'VAR'   }
            item['TITLE'    ] = {'SK': apology          , 'TYPE':'H2'    }
            item['NARR'     ] = {'SK': "Unknown"        , 'TYPE':'H3'    }
            item['D_CRT'    ] = {'SK': 'now'            , 'TYPE':'DATE'  }
            item['D_CHG'    ] = {'SK': 'now'            , 'TYPE':'DATE'  }
            item['TEXT'     ] = {'SK': ''               , 'TYPE':'P'     }

        #----------------------------------------------------------------------
        self.journal.O()
        return (data, item)

    #--------------------------------------------------------------------------
    def loadForumSiblings(self, who, forumId, parIdx, idx, target):
    
        self.journal.I(f"{self.name}.loadForumSiblings: For item {forumId}.{parIdx}")
        toRet = []

        #----------------------------------------------------------------------
        # Zoznam posledne zmenenych itemov pre root item, inak siblings
        #----------------------------------------------------------------------
        if parIdx == 0: toRet.append( {'SibsLabel':{'SK': 'Nedávno zmenené kapitoly', 'TYPE':'LABEL', 'style':'width:14em;' }} )
        else: 
            #------------------------------------------------------------------
            # Nacitam parenta z DB
            #------------------------------------------------------------------
            parentData, parentItem = self.loadForumItem(who, forumId, idx=parIdx, target=target)
            
            atts = {}
            atts['SK'   ] = f" << {parentItem['TITLE']['SK']} <<"
            atts['TYPE' ] = 'A'
            atts['URL'  ] = target
            atts['IDX'  ] = str(parIdx)
            atts['style'] = "text-align:center; font-style:italic;"
            atts['BREAK'] = True
            
            toRet.append( {'SibsLabel':atts} )

        toRet.append( {'SibsSplit':{'TYPE':'SPLIT'}} )
        
        #----------------------------------------------------------------------
        # Nacitam siblings z DB
        #----------------------------------------------------------------------
        data = self.readForumChildren(who, forumId, parIdx=parIdx)

        #----------------------------------------------------------------------
        # Konverzia nacitanych riadkov z DB do itemov
        #----------------------------------------------------------------------
        i = 0
        for row in data:

            curIdx = str(row[0])
            func   = row[1]
            title  = row[2]
            
            #------------------------------------------------------------------
            # Pre koncepty vlozim pred titul C
            #------------------------------------------------------------------
            if func   == 'K'     : title = f"C {title}"
            
            if curIdx == str(idx): title = f">> {title}"
        
            toRet.append( {f"sibl_{i}": {'class':'smallFont', 'SK':title[:_TITLE_MAX], 'TYPE':'A', 'URL':target, 'IDX':curIdx, 'BREAK':True }} )

            i += 1
      
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def loadForumChildren(self, who, forumId, idx, target):
    
        self.journal.I(f"{self.name}.loadForumChildren: {forumId}.{idx}")
        toRet = []

        #----------------------------------------------------------------------
        # Zoznam podkapitol
        #----------------------------------------------------------------------
        toRet.append( {'ChildLabel':{'SK': 'Podkapitoly',  'TYPE':'LABEL' }} )
        toRet.append( {'ChildSplit':{'TYPE':'SPLIT'}} )
        
        #----------------------------------------------------------------------
        # Nacitam children z DB
        #----------------------------------------------------------------------
        data = self.readForumChildren(who, forumId, parIdx=idx)
        
        #----------------------------------------------------------------------
        # Konverzia nacitanych riadkov z DB do itemov
        #----------------------------------------------------------------------
        i = 0
        for row in data:

            idx   = str(row[0])
            func  = row[1]
            title = row[2]
            
            #------------------------------------------------------------------
            # Pre koncepty vlozim pred titul C
            #------------------------------------------------------------------
            if func=='K': title = f"C {title}"
        
            toRet.append( {f"child_{i}": {'class':'smallFont', 'SK':title[:_TITLE_MAX], 'TYPE':'A', 'URL':target, 'IDX':idx, 'BREAK':True }} )

            i += 1
      
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def readForumChildren(self, who, forumId, parIdx, days=_DAY_CHANGES):
        "Reads from DB items for respective <parIdx> and changed in last <days>"
    
        self.journal.I(f"{self.name}.readForumChildren: {forumId}.{parIdx} in last {days} days")

        #----------------------------------------------------------------------
        # Zoznam posledne zmenenych itemov pre root item, inak siblings
        #----------------------------------------------------------------------
        if parIdx == 0: where = f" FORUM_ID = '{forumId}' and julianday('now')-julianday(d_changed) <= {days}"
        else          : where = f" FORUM_ID = '{forumId}' and PARENT_ID = {str(parIdx)}"

        #----------------------------------------------------------------------
        # Nacitanie zoznamu TITLEs z DB ako list
        #----------------------------------------------------------------------
        sql = f"select ITEM_ID, C_FUNC, TITLE from {Config.tabForum} where {where} order by TITLE"
        children = self.readDb(who=who, sql=sql)
        
        #----------------------------------------------------------------------
        self.journal.O()
        return children

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal         import SiqoJournal
    
    journal = SiqoJournal('test-DMS', debug=4)
    
    dms = DMS(journal, Config.dtbsName, Config.dtbsPath)
    
    docs = dms.docRead('ja')
    doc  = dms.docById('ja', 57)
    

#==============================================================================
# Test cases
#------------------------------------------------------------------------------

#==============================================================================
print(f"app_dms {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
