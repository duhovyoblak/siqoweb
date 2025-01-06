#==============================================================================
#                                                     (c) SIQO 24
# Class Forum for SIQO Flask application
#
#------------------------------------------------------------------------------
import re
import traceback

from   datetime                 import date
from   flask                    import request, redirect

from   siqoweb.w__window        import Window
from   siqoweb.w_forum_f        import ForumForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.11'

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
    def __init__(self, journal, dms, userId, lang, item, POST, idx):

        journal.I(f"Forum.__init__: From {item} for {userId}")

        #----------------------------------------------------------------------
        # Inicializacia Window
        #----------------------------------------------------------------------
        super().__init__(journal, dms, userId, lang, item, POST, idx)

        self.winClass  = 'Forum'        # Window's class for response generator

        self.journal.O()

    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost:")

        #----------------------------------------------------------------------
        # Vyhodnotim formular
        #----------------------------------------------------------------------
        #if self.form.validate_on_submit():
        if self.form.validate():
            
            #------------------------------------------------------------------
            # Cancel
            #------------------------------------------------------------------
            if self.form.sfCancel.data:
                
                self.journal.M(f"{self.name}.respPost: Cancel by user")
                self.journal.O()
                return redirect(f"{self.urlFor(self.target)}/{self.idx}")
            
            #------------------------------------------------------------------
            # Apply
            #------------------------------------------------------------------
            if self.form.sfApply.data:
                
                self.journal.M(f"{self.name}.respPost: Apply changes")
                
                #--------------------------------------------------------------
                # Ziskam udaje z formulara
                #--------------------------------------------------------------
                self.dbData['PARENT_ID'] = self.form.parentId.data
                self.dbData['USER_ID'  ] = self.form.userId.data
                self.dbData['TITLE'    ] = self.form.title.data
                self.dbData['NARRATOR' ] = self.form.narrator.data
                self.dbData['ITEM'     ] = self.form.text.data

                #--------------------------------------------------------------
                # Zapisem zmeny do DB
                #--------------------------------------------------------------
                self.dms.saveForumItem(who=self.userId, forumId=self.objId, data=self.dbData)
                
                self.journal.O()
                return redirect(f"{self.urlFor(self.target)}/{self.idx}")
            
            #------------------------------------------------------------------
            # Unknown user's action
            #------------------------------------------------------------------
            else:
                self.journal.O()
                return redirect(f"{self.urlFor(self.target)}/{self.idx}")
 
        #----------------------------------------------------------------------
        # Nie je POST
        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.respPost: form NOT validated with errors:", True)
        self.journal.M(f"{self.name}.respPost: {self.form.errors}", True)

        self.journal.O()
        return self.toHomepage()

    
    #==========================================================================
    # Form methods
    #--------------------------------------------------------------------------
    def resolvePost(self):
        "This method resolves dynamic POST data"
        
        self.journal.I(f"{self.name}.resolvePost:")
        
        #----------------------------------------------------------------------
        # Vyhodnotenie dynamickeho kontextu z POST data
        #----------------------------------------------------------------------
        if 'itemId' in self.POST.keys(): 
            
            lastIdx  = self.idx
            self.idx = int(self.POST['itemId'])
            self.journal.M(f"{self.name}.resolvePost    : idx was changed from {lastIdx} to {self.idx}", True)

        self.journal.O()

    #--------------------------------------------------------------------------
    def formFromPost(self):
        "This method cretes form based on POST data"
        
        self.journal.I(f"{self.name}.formFromPost:")
        self.journal.M(f"{self.name}.formFromPost   : formType='ForumForm', userId={self.dbData['USER_ID']}, itemId={self.idx}", True)
        
        #----------------------------------------------------------------------
        # Vytvorenie Forum formulara z post data
        #----------------------------------------------------------------------
        try   : self.form = ForumForm(formdata=self.POST, formType="ForumForm", userId=self.dbData['USER_ID'], itemId=str(self.idx))
        except: self.journal.M(f"{self.name}.formFromPost   : Ouside context, form was not created", True)

        self.journal.O()

    #--------------------------------------------------------------------------
    def formDataFromDb(self):
        "This method loads tuple (dbItem, dbData) from DMS/Database"
        
        self.journal.I(f"{self.name}.formDataFromDb:")

        self.dbData    = None                  # Data content from DMS/Formular
        self.dbItem    = None                  # Item content from DMS
    
        self.journal.M(f"{self.name}.formDataFromDb : forumId={self.objId}, idx={self.idx}", True)

        #----------------------------------------------------------------------
        # Nacitanie objektu podla class/objId/idx
        #----------------------------------------------------------------------
        self.dbData, self.dbItem = self.dms.loadForumItem(self.name, forumId=self.objId, idx=self.idx, target=self.target)
      
        if self.dbItem is None:
            self.journal.M(f"{self.name}.formDataFromDb : No dbItem for class={self.classId}, object={self.objId} with idx={self.idx}", True)

        #----------------------------------------------------------------------
        self.journal.O()
        return (self.dbData, self.dbItem)
    
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
        toRet += str(self.form.itemId.label())
        toRet += str(self.form.itemId( value=self.dbData['ITEM_ID']))
        toRet += self.breakLine()

        toRet += str(self.form.title.label())
        toRet += str(self.form.title(    class_="ObjectInputString", value=self.dbData['TITLE']))
        toRet += self.breakLine()

        toRet += str(self.form.parentId.label())
        toRet += str(self.form.parentId(  class_="ObjectInputString", value=self.dbData['PARENT_ID'], size=35))
        toRet += self.breakLine()

        toRet += str(self.form.userId.label())
        toRet += str(self.form.userId(  class_="ObjectInputString", value=self.dbData['USER_ID'], size=35))
        toRet += self.breakLine()

        toRet += str(self.form.narrator.label())
        toRet += str(self.form.narrator( class_="ObjectInputString", value=self.dbData['NARRATOR'], size=35))
        toRet += self.breakLine()
          
        toRet += str(self.form.text.label())
        self.form.text.data = self.dbData['ITEM']
        toRet += str(self.form.text(class_="ObjectInputText", rows="20"))

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

#        toRet += str(self.form.sfUp        (class_="ObjectControlBtn", disabled="disabled" ))
#        toRet += str(self.form.sfAddChapter(class_="ObjectControlBtn"))
#        toRet += str(self.form.afAddChild  (class_="ObjectControlBtn"))
        toRet += str(self.form.sfCancel    (class_="ObjectControlBtn"))
        toRet += str(self.form.sfApply     (class_="ObjectControlBtn"))
#        toRet += str(self.form.sfPublish   (class_="ObjectControlBtn"))
#        toRet += str(self.form.sfDelete    (class_="ObjectControlBtn"))
#        toRet += str(self.form.sfMove      (class_="ObjectControlBtn"))

        #----------------------------------------------------------------------
        return toRet
    
#==============================================================================
print(f"Forum {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
