#==============================================================================
#                                                     (c) SIQO 24
# Class Window for SIQO Flask application
#
#------------------------------------------------------------------------------
import os
import re
import traceback

from   datetime                 import date
from   flask                    import request, url_for

from   o__object                import Object
from   f_window                 import FormWindow

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.10'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
#journal = None
#db      = None

#==============================================================================
# Class Window
#------------------------------------------------------------------------------
class Window(Object):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dms, userId, lang, item, height=20, width=20):

        #----------------------------------------------------------------------
        # Define parameters of the ItemDef
        #----------------------------------------------------------------------
        (itemDef, self.classId ) = self.itemDrop(item, 'CLASS' )  
        (itemDef, self.objId   ) = self.itemDrop(item, 'objId' )
        (itemDef, self.target  ) = self.itemDrop(item, 'target')
        (itemDef, self.crForm  ) = self.itemDrop(item, 'crForm')
        
        (itemDef, self.height  ) = self.itemDrop(item, 'height')
        (itemDef, self.width   ) = self.itemDrop(item, 'width' )
        
        if self.width  == '': self.width  = '99%'
        if self.height == '': self.height = '94%'

        #----------------------------------------------------------------------
        # Inicializacia Objectu
        #----------------------------------------------------------------------
        super().__init__(journal, dms, userId, lang, self.classId, height=height, width=width) # classId=OBJECT_ID v pagman db

        self.journal   = journal
        self.name      = f"Win({self.name})"
        
        self.itemDef   = item                  # Item dict definition from DB
        self.dbData    = None                  # Data content from DMS/Formular
        self.dbItem    = None                  # Item content from DMS
        
        self.form      = None                  # Formular for this window
        self.postForm  = None                  # Data from POST request.form
        self.postForm  = request.form
       
        #----------------------------------------------------------------------
        # Dynamicky prenasane parametre
        #----------------------------------------------------------------------


    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def load(self, idx):
        """"This method should be overrided and load tuple (dbItem, dbData) 
            from DMS/Database"""
        
        self.dbData    = None                  # Data content from DMS/Formular
        self.dbItem    = None                  # Item content from DMS
    
        #----------------------------------------------------------------------
        # Nacitanie objektu podla class
        #----------------------------------------------------------------------
        self.dbData, self.dbItem = self.dms.loadForumItem(self.name, forumId=self.objId, idx=idx, target=self.target)
      
        if self.dbItem is None:
            
            self.journal.M(f"HTML_{self.name}.load: No dbItem for class={self.classId}, object={self.objId} with idx={idx}", True)

        #----------------------------------------------------------------------
        return (self.dbData, self.dbItem)
    
    #--------------------------------------------------------------------------
    def saveDbItem(self, dbItem):
        
       
        #----------------------------------------------------------------------
        print('dbItem > ', dbItem)
    
    #==========================================================================
    # Rendering API for templates
    #--------------------------------------------------------------------------
    def html(self, objDic, lang):
        "Returns HTML for json-encoded item"
        
        self.journal.I(f"HTML_{self.name}.html: Going to render an object dictionary...")
        toRet = ''
    
        #----------------------------------------------------------------------
        # Prejdem vsetky objekty
        #----------------------------------------------------------------------
        for objId, rec in objDic.items():
            
            #------------------------------------------------------------------
            # Ak je rec typu dict, ide o vnoreny objekt
            #------------------------------------------------------------------
            if type(rec)==dict:
              
                #--------------------------------------------------------------
                # Rekurzivne zavolam objectsRender
                #--------------------------------------------------------------
                toRet += self.html(rec, lang)
                
            #------------------------------------------------------------------
            # Ak je rec typu list, ide o zoznam itemov
            #------------------------------------------------------------------
            elif type(rec)==list:
              
                #--------------------------------------------------------------
                # Zavolam itemListRender
                #--------------------------------------------------------------
                toRet += self.itemListRender(rec, lang, objId)
            
            #------------------------------------------------------------------
            # Inak je to neznamy udaj
            #------------------------------------------------------------------
            else:
                self.journal.M(f"HTML_{self.name}.html: UNKNOWN object '{objDic}'", True)

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
        
    #==========================================================================
    # HTML methods
    #--------------------------------------------------------------------------
#!!!!
    def html(self):
        "Returns html code for this Window"
        
        toRet = ''
  
        #----------------------------------------------------------------------
        # Kontrola existencie dbItem
        #----------------------------------------------------------------------
        if self.dbItem is None:
            self.journal.M(f"HTML_{self.name}.dbObject: No dbItem defined", True)
            return toRet

        #----------------------------------------------------------------------
        # Object space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_OS", "class":"Object", "style":f"height:{self.height}; width:{self.width};"}
        toRet += self.divStart(atts)

        #----------------------------------------------------------------------
        # Header space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_HS", "class":"ObjectHeaderSpace", "onclick":f"ObjectContentControl('{self.objId}', '20')"}
        toRet += self.divStart(atts)
        toRet += self.objectHead()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Back space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_BS", "class":"ObjectBackSpace", "style":"height:0px;"}
        toRet += self.divStart(atts)
        toRet += self.objectBack()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Front space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_FS", "class":"ObjectFrontSpace", "style":f"height:{self.height};"}
        toRet += self.divStart(atts)
        toRet += self.objectFront()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Control space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_CS", "class":"ObjectControlSpace"}
        toRet += self.divStart(atts)
        toRet += self.objectControll()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Object space end
        #----------------------------------------------------------------------
        toRet += self.divStop()

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlHead(self):
        """"This method should be overrided and return html code
            for the head space of this window"""
        
        toRet = ''
        
        #----------------------------------------------------------------------
        # Vytvorenie hlavicky objektu podla class
        #----------------------------------------------------------------------
        (self.dbItem, title) = self.itemDrop(self.dbItem, 'TITLE')
        toRet += self.itemRender(title, self.lang)

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlBack(self, objClass, item, dbItem, dbData, lang):
        """"This method should be overrided and return html code
            for the back space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Render the object formular
        #----------------------------------------------------------------------
            
        method = 'POST'
        action = url_for(self.target)
        toRet += self.formStart({"method":method, "action":action, "enctype":"multipart/form-data"})
            
        toRet += str(self.dynForms[0].itemId.label())
        toRet += str(self.dynForms[0].itemId( value=dbData['ITEM_ID']))
        toRet += self.breakLine()

        toRet += str(self.dynForms[0].title.label())
        toRet += str(self.dynForms[0].title(    class_="ObjectInputString", value=dbData['TITLE']))
        toRet += self.breakLine()

        toRet += str(self.dynForms[0].user_id.label())
        toRet += str(self.dynForms[0].user_id(  class_="ObjectInputString", value=dbData['USER_ID'], size=35))
        toRet += self.breakLine()

        toRet += str(self.dynForms[0].narrator.label())
        toRet += str(self.dynForms[0].narrator( class_="ObjectInputString", value=dbData['NARRATOR'], size=35))
        toRet += self.breakLine()

          
        toRet += str(self.dynForms[0].item.label())
        self.dynForms[0].item.data = dbData['ITEM']
        toRet += str(self.dynForms[0].item(class_="ObjectInputText", rows="20"))

        toRet += str(self.dynForms[0].hidden_tag())

        self.formStop()

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlFront(self, objClass, item, dbItem, lang):

        toRet = ''

        #----------------------------------------------------------------------
        # Vytvorenie Front/end objektu podla class
        #----------------------------------------------------------------------
        if objClass == 'FORUM':
            
            (self.itemDef, ForumId) = self.itemDrop(  item, 'Forum'    )
            (self.itemDef, target ) = self.itemDrop(  item, 'target'   )

            (dbItem, objId) = self.itemDrop(dbItem, 'ITEM_ID'  )
            (dbItem, parId) = self.itemDrop(dbItem, 'PARENT_ID')
            (dbItem, narr ) = self.itemDrop(dbItem, 'NARR'     )
            (dbItem, d_crt) = self.itemDrop(dbItem, 'D_CRT'    )
            (dbItem, d_chg) = self.itemDrop(dbItem, 'D_CHG'    )
            (dbItem, text ) = self.itemDrop(dbItem, 'TEXT'     )
            
            
            idx    = objId['SK']
            parIdx = parId['SK']

#            print('idx,    ', idx)
#            print('parIdx, ', parIdx)
            
            #------------------------------------------------------------------
            # Vykreslenie Siblings/Changes
            #------------------------------------------------------------------
            toRet += self.divStart({"class":"Selector", "style":"height:100%; width:20%; display:block"})
            sibs   = self.dms.loadForumSiblings(who='ja', ForumId=ForumId, parIdx=parIdx, idx=idx, target=target)
            toRet += self.itemListRender(sibs, lang)
            toRet += self.divStop()
            
            #------------------------------------------------------------------
            # Vykreslenie Vykreslenie Forum itemu
            #------------------------------------------------------------------
            toRet += self.divStart({"class":"ForumItem", "style":"height:100%; width:60%; display:block"})
            toRet += self.itemRender(narr,  lang)
            toRet += self.itemRender(d_chg, lang)

            # Finalne vykreslenie textu
            toRet += self.itemRender(text,  lang)
            toRet += self.divStop()
            
            #------------------------------------------------------------------
            # Vykreslenie Children
            #------------------------------------------------------------------
            toRet += self.divStart({"class":"Selector", "style":"height:100%; width:20%; display:block"})
            child  = self.dms.loadForumChildren(who='ja', ForumId=ForumId, idx=idx, target=target)
            toRet += self.itemListRender(child, lang)
            toRet += self.divStop()
            
        else: 
            (dbItem, objName) = self.itemDrop(dbItem, lang)
            toRet += self.p({lang:objName}, lang)

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlControll(self, objClass, item, dbItem, lang):

        toRet = ''

        if objClass == 'FORUM':
            
            toRet += str(self.dynForms[0].sfUp        (class_="ObjectControlBtn"))
            toRet += str(self.dynForms[0].sfAddChapter(class_="ObjectControlBtn"))
            toRet += str(self.dynForms[0].afAddChild  (class_="ObjectControlBtn"))
            toRet += str(self.dynForms[0].sfCancel    (class_="ObjectControlBtn"))
            toRet += str(self.dynForms[0].sfApply     (class_="ObjectControlBtn"))
            toRet += str(self.dynForms[0].sfPublish   (class_="ObjectControlBtn"))
            toRet += str(self.dynForms[0].sfDelete    (class_="ObjectControlBtn"))
            toRet += str(self.dynForms[0].sfMove      (class_="ObjectControlBtn"))

        else: 
            (dbItem, objName) = self.itemDrop(dbItem, lang)
            toRet += self.p({lang:objName}, lang)

        #----------------------------------------------------------------------
        return toRet

    
#==============================================================================
print(f"Window {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
