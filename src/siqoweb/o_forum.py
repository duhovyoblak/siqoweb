#==============================================================================
#                                                     (c) SIQO 24
# Class Forum for SIQO Flask application
#
#------------------------------------------------------------------------------
import os
import re
import traceback

from   datetime                 import date
from   flask                    import request, url_for

from   o__object                import Object
from   f_forum                  import FormForum

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
# Class Forum
#------------------------------------------------------------------------------
class Forum(Object):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, userId, lang, classId, height=20, width=20):

        #----------------------------------------------------------------------
        # Inicializacia Objectu
        #----------------------------------------------------------------------
        super().__init__(journal, dms, userId, lang, classId)  # classId=OBJECT_ID v pagman db

        
        self.journal   = journal
        self.who       = who   
        self.dms       = dms       # DMS manager
        self.classId   = classId   # OBJECT_ID v pagman db
        
        #----------------------------------------------------------------------
        # Dynamicky prenasane parametre
        #----------------------------------------------------------------------
        self.dynIdx    = 0
        self.dynForms  = []

    #==========================================================================
    # Rendering API for templates
    #--------------------------------------------------------------------------
    def objectsRender(self, objDic, lang):
        "Returns HTML for json-encoded item"
        
        self.journal.I(f"HTML_{self.who}.objectsRender: Going to render an object dictionary...")
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
                toRet += self.objectsRender(rec, lang)
                
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
                self.journal.M(f"HTML_{self.who}.objectsRender: UNKNOWN object '{objDic}'", True)

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
        
    #==========================================================================
    # DB Objects block
    #--------------------------------------------------------------------------
#!!!!
    def dbObject(self, item, lang):
        """Renders objects based on parameters"""
        
        toRet = ''
        
        #----------------------------------------------------------------------
        # Define parameters of an object
        #----------------------------------------------------------------------
        (item, objClass ) = self.itemDrop(item, 'CLASS' )
        (item, target   ) = self.itemDrop(item, 'target')
        (item, crForm   ) = self.itemDrop(item, 'crForm')
        
        (item, objId    ) = self.itemDrop(item, 'objId' )
        (item, height   ) = self.itemDrop(item, 'height')
        (item, width    ) = self.itemDrop(item, 'width' )
        
        if width  == '': width  = '99%'
        if height == '': height = '94%'
  
        #----------------------------------------------------------------------
        # Read instance of the object for respective class
        #----------------------------------------------------------------------
        dbData, dbItem = self.loadDbItem(who='ja', objClass=objClass, item=item)
        
        if dbItem is None:
            
            self.journal.M(f"HTML_{self.who}.dbObject: No dbItem for class={objClass} and item={item}", True)
            return toRet

        #----------------------------------------------------------------------
        # Object space
        #----------------------------------------------------------------------
        atts = {"name":objId, "id":f"{objId}_OS", "class":"Object", "style":f"height:{height}; width:{width};"}
        toRet += self.divStart(atts);

        #----------------------------------------------------------------------
        # Header space
        #----------------------------------------------------------------------
        atts = {"name":objId, "id":f"{objId}_HS", "class":"ObjectHeaderSpace", "onclick":f"ObjectContentControl('{objId}', '20')"}
        toRet += self.divStart(atts);
        toRet += self.objectHead(objClass, item=item, dbItem=dbItem, lang=lang)
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Back space
        #----------------------------------------------------------------------
        atts = {"name":objId, "id":f"{objId}_BS", "class":"ObjectBackSpace", "style":"height:0px;"}
        toRet += self.divStart(atts);
        toRet += self.objectBack(objClass, item=item, dbItem=dbItem, dbData=dbData, lang=lang)
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Front space
        #----------------------------------------------------------------------
        atts = {"name":objId, "id":f"{objId}_FS", "class":"ObjectFrontSpace", "style":f"height:{height};"}
        toRet += self.divStart(atts);
        toRet += self.objectFront(objClass, item=item, dbItem=dbItem, lang=lang)
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Control space
        #----------------------------------------------------------------------
        atts = {"name":objId, "id":f"{objId}_CS", "class":"ObjectControlSpace"}
        toRet += self.divStart(atts);
        toRet += self.objectControll(objClass, item=item, dbItem=dbItem, lang=lang)
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Object space end
        #----------------------------------------------------------------------
        toRet += self.divStop()

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def loadDbItem(self, who, objClass, item):
        
        dbData = None
        dbItem = None
    
        #----------------------------------------------------------------------
        # Nacitanie objektu podla class
        #----------------------------------------------------------------------
        if objClass == 'FORUM':
            
            (item, forumId) = self.itemDrop(item, 'FORUM' )
            (item, target ) = self.itemDrop(item, 'target')
            
            dbData, dbItem = self.dms.loadForumItem(who, forumId=forumId, idx=self.dynIdx, target=target)
      
        #----------------------------------------------------------------------
        return (dbData, dbItem)
    
    #--------------------------------------------------------------------------
    def saveDbItem(self, who, dbItem):
        
       
        #----------------------------------------------------------------------
        print('dbItem > ', dbItem)
    
    #--------------------------------------------------------------------------
    def objectHead(self, objClass, item, dbItem, lang):
        
        toRet = ''
        
        #----------------------------------------------------------------------
        # Vytvorenie hlavicky objektu podla class
        #----------------------------------------------------------------------
        if objClass == 'FORUM':
            
            (dbItem, title) = self.itemDrop(dbItem, 'TITLE')
            toRet += self.itemRender(title, lang)

        else: 
            (dbItem, objName) = self.itemDrop(dbItem, lang)
            toRet += self.p({lang:objName}, lang)

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def objectBack(self, objClass, item, dbItem, dbData, lang):

        toRet = ''

        #----------------------------------------------------------------------
        # Vytvorenie Front/end objektu podla class
        #----------------------------------------------------------------------
        if objClass == 'FORUM':
            
            (item,   target) = self.itemDrop(  item, 'target'   )
            
            #------------------------------------------------------------------
            # Render the object formular
            #------------------------------------------------------------------
            method = 'POST'
            action = url_for(target)
            toRet += self.formStart({"method":method, "action":action, "enctype":"multipart/form-data"})
            
            #toRet += str(self.dynForms[0].parentId.label())
            #toRet += str(self.dynForms[0].parentId( value=dbData['PARENT_ID']))
            #toRet += self.breakLine()

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
            #------------------------------------------------------------------
            
        else: 
            (dbItem, objName) = self.itemDrop(dbItem, lang)
            toRet += self.p({lang:objName}, lang)

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def objectFront(self, objClass, item, dbItem, lang):

        toRet = ''

        #----------------------------------------------------------------------
        # Vytvorenie Front/end objektu podla class
        #----------------------------------------------------------------------
        if objClass == 'FORUM':
            
            (item, forumId) = self.itemDrop(  item, 'FORUM'    )
            (item, target ) = self.itemDrop(  item, 'target'   )

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
            sibs   = self.dms.loadForumSiblings(who='ja', forumId=forumId, parIdx=parIdx, idx=idx, target=target)
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
            child  = self.dms.loadForumChildren(who='ja', forumId=forumId, idx=idx, target=target)
            toRet += self.itemListRender(child, lang)
            toRet += self.divStop()
            
        else: 
            (dbItem, objName) = self.itemDrop(dbItem, lang)
            toRet += self.p({lang:objName}, lang)

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def objectControll(self, objClass, item, dbItem, lang):

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

    #--------------------------------------------------------------------------
    
#==============================================================================
print(f"Forum {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
