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

from   w__window                import Window
from   w_forum_f                import ForumForm

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
class Forum(Window):
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dms, userId, lang, item, postForm, idx):

        journal.I(f"Forum.__init__: From {item} for {userId}")

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
        # Inicializacia Window
        #----------------------------------------------------------------------
        super().__init__(journal, dms, userId, lang, item=item, postForm=postForm, idx=idx) # classId=OBJECT_ID v pagman db

        self.name      = f"Forum({self.name})"
        self.formId    = f"ForumForm_{self.idx}"  # Id of the formular
       
        #----------------------------------------------------------------------
        # Nacitanie formulara s POST udajmi
        #----------------------------------------------------------------------
#        self.loadForm()

        self.journal.O()

    #==========================================================================
    # Form methods
    #--------------------------------------------------------------------------
    def loadForm(self):
        "This method should return class specific content like forms, objects etc."
        
        self.journal.I(f"{self.name}.loadForm:")
        
        #----------------------------------------------------------------------
        # Ziskanie post data
        #----------------------------------------------------------------------
        self.formPost  = request.form

        #----------------------------------------------------------------------
        # Vytvorenie Forum formulara z post data
        #----------------------------------------------------------------------
        self.form = ForumForm(formdata=self.formPost, formType="LoginForm", target=self.target, itemId=self.idx)

        self.journal.O()

    #==========================================================================
    # DB Persistency methods
    #--------------------------------------------------------------------------
    def dbLoad(self):
        """"This method should be overrided and load tuple (dbItem, dbData) 
            from DMS/Database"""
        
        self.dbData    = None                  # Data content from DMS/Formular
        self.dbItem    = None                  # Item content from DMS
    
        #----------------------------------------------------------------------
        # Nacitanie objektu podla class/objId/idx
        #----------------------------------------------------------------------
        self.dbData, self.dbItem = self.dms.loadForumItem(self.name, forumId=self.objId, idx=self.idx, target=self.target)
      
        if self.dbItem is None:
            
            self.journal.M(f"HTML_{self.name}.dbLoad: No dbItem for class={self.classId}, object={self.objId} with idx={self.idx}", True)

        #----------------------------------------------------------------------
        return (self.dbData, self.dbItem)
    
    #--------------------------------------------------------------------------
    def dbSave(self):
        """"This method should be overrided and save dbData 
            into DMS/Database"""
        
       
        #----------------------------------------------------------------------
        print('dbData > ', self.dbData)
    
    #==========================================================================
    # HTML methods
    #--------------------------------------------------------------------------
#!!!!
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
    def htmlBack(self):
        """"This method should be overrided and return html code
            for the back space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Render the object formular
        #----------------------------------------------------------------------
        method = 'POST'
        action = url_for(self.target)
        toRet += self.formStart({"method":method, "action":action, "enctype":"multipart/form-data"})
            
        toRet += str(self.form.itemId.label())
        toRet += str(self.form.itemId( value=self.dbData['ITEM_ID']))
        toRet += self.breakLine()

        toRet += str(self.form.title.label())
        toRet += str(self.form.title(    class_="ObjectInputString", value=self.dbData['TITLE']))
        toRet += self.breakLine()

        toRet += str(self.form.user_id.label())
        toRet += str(self.form.user_id(  class_="ObjectInputString", value=self.dbData['USER_ID'], size=35))
        toRet += self.breakLine()

        toRet += str(self.form.narrator.label())
        toRet += str(self.form.narrator( class_="ObjectInputString", value=self.dbData['NARRATOR'], size=35))
        toRet += self.breakLine()
          
        toRet += str(self.form.item.label())
        self.form.item.data = self.dbData['ITEM']
        toRet += str(self.form.item(class_="ObjectInputText", rows="20"))

        toRet += str(self.form.hidden_tag())

        self.formStop()

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlFront(self):
        """"This method should be overrided and return html code
            for the front space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Vytvorenie Front/end objektu podla class
        #----------------------------------------------------------------------
        (self.dbItem, objId) = self.itemDrop(self.dbItem, 'ITEM_ID'  )
        (self.dbItem, parId) = self.itemDrop(self.dbItem, 'PARENT_ID')
        (self.dbItem, narr ) = self.itemDrop(self.dbItem, 'NARR'     )
        (self.dbItem, d_crt) = self.itemDrop(self.dbItem, 'D_CRT'    )
        (self.dbItem, d_chg) = self.itemDrop(self.dbItem, 'D_CHG'    )
        (self.dbItem, text ) = self.itemDrop(self.dbItem, 'TEXT'     )
            
            
        idx    = objId['SK']
        parIdx = parId['SK']

#        print('idx,    ', idx)
#        print('parIdx, ', parIdx)
            
        #----------------------------------------------------------------------
        # Vykreslenie Siblings/Changes
        #----------------------------------------------------------------------
        toRet += self.divStart({"class":"Selector", "style":"height:100%; width:20%; display:block"})
        sibs   = self.dms.loadForumSiblings(self.name, forumId=self.objId, parIdx=parIdx, idx=idx, target=self.target)
        toRet += self.itemListRender(sibs, self.lang)
        toRet += self.divStop()
            
        #----------------------------------------------------------------------
        # Vykreslenie Vykreslenie Forum itemu
        #----------------------------------------------------------------------
        toRet += self.divStart({"class":"ForumItem", "style":"height:100%; width:60%; display:block"})
        toRet += self.itemRender(narr,  self.lang)
        toRet += self.itemRender(d_chg, self.lang)

        # Finalne vykreslenie textu
        toRet += self.itemRender(text,  self.lang)
        toRet += self.divStop()
            
        #----------------------------------------------------------------------
        # Vykreslenie Children
        #----------------------------------------------------------------------
        toRet += self.divStart({"class":"Selector", "style":"height:100%; width:20%; display:block"})
        child  = self.dms.loadForumChildren(self.name, forumId=self.objId, idx=idx, target=self.target)
        toRet += self.itemListRender(child, self.lang)
        toRet += self.divStop()
            
        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlControll(self):
        """"This method should be overrided and return html code
            for the controll space of this window"""

        toRet = ''

        toRet += str(self.form.sfUp        (class_="ObjectControlBtn"))
        toRet += str(self.form.sfAddChapter(class_="ObjectControlBtn"))
        toRet += str(self.form.afAddChild  (class_="ObjectControlBtn"))
        toRet += str(self.form.sfCancel    (class_="ObjectControlBtn"))
        toRet += str(self.form.sfApply     (class_="ObjectControlBtn"))
        toRet += str(self.form.sfPublish   (class_="ObjectControlBtn"))
        toRet += str(self.form.sfDelete    (class_="ObjectControlBtn"))
        toRet += str(self.form.sfMove      (class_="ObjectControlBtn"))

        #----------------------------------------------------------------------
        return toRet

    
#==============================================================================
print(f"Forum {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
