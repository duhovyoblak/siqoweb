#==============================================================================
#                                                     (c) SIQO 24
# Class Window for SIQO Flask application
#
#------------------------------------------------------------------------------
import re
import traceback

from   datetime                 import date
from   flask                    import request, session, abort, redirect

from   o__object                import Object
from   w__window_f              import WindowForm

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
    # Staticke premenne
    #--------------------------------------------------------------------------
    wins = {}
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dms, userId, lang, item, POST, idx):

        journal.I(f"Window.__init__: From {item} for {userId}")

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
        super().__init__(journal, dms, userId, lang, classId=self.classId, height=self.height, width=self.width) # classId=OBJECT_ID v pagman db

        (itemDef, name) = self.itemDrop(item, 'NAME')  
        
        self.name      = name                     # Unique window's name
        self.winClass  = 'Window'                 # Window's class for response generator
        self.itemDef   = item                     # Item dict definition from DB
        self.POST      = POST                     # Data from POST request.form
        self.idx       = idx                      # Primarny kluc objektu
        
        self.dbData    = None                     # Data content from DMS/Formular
        self.dbItem    = None                     # Item content from DMS
        
        self.form      = None                     # Formular asociated with this window
       
        #----------------------------------------------------------------------
        # Vytvorenie formulara s POST udajmi a nacitenie jeho obrazu z DB
        #----------------------------------------------------------------------
        self.resolvePost()
        self.formDataFromDb()
        self.formFromPost()

        #----------------------------------------------------------------------
        self.journal.O()

    #--------------------------------------------------------------------------
    def info(self, lvl=2):
        "Returns info about the Window"

        toRet = [f"{3*' '*lvl}{self.name}> {self.classId}.{self.objId}({self.idx}) {self.width}x{self.height}"]
        toRet.append('\n')
        
        return toRet

    #==========================================================================
    # Form methods
    #--------------------------------------------------------------------------
    def resolvePost(self):
        "This method resolves dynamic POST data"
        
        self.journal.I(f"{self.name}.resolvePost:")
        
        #----------------------------------------------------------------------
        # Vyhodnotenie dynamickeho kontextu z POST data
        #----------------------------------------------------------------------
        "This section should be overrided"

        self.journal.O()

    #--------------------------------------------------------------------------
    def formFromPost(self):
        "This method cretes form based on POST data"
        
        self.journal.I(f"{self.name}.formFromPost:")
        
        #----------------------------------------------------------------------
        # Vytvorenie window formulara z post data
        #----------------------------------------------------------------------
        "This section should be overrided"

        self.journal.O()

    #--------------------------------------------------------------------------
    def formDataFromDb(self):
        "This method loads tuple (dbItem, dbData) from DMS/Database"
        
        self.dbData    = None                  # Data content from DMS/Formular
        self.dbItem    = None                  # Item content from DMS
    
        #----------------------------------------------------------------------
        # Nacitanie objektu podla class/objId/idx
        #----------------------------------------------------------------------
        "This section should be overrided"
      
        #----------------------------------------------------------------------
        return (self.dbData, self.dbItem)
    
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
        # Form start
        #----------------------------------------------------------------------
        method = 'POST'
        action = self.urlFor(self.target)
        toRet += self.formStart({"method":method, "action":action, "enctype":"multipart/form-data", "style":"display:contents;"})

        #----------------------------------------------------------------------
        # Header space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_HS", "class":"ObjectHeaderSpace", "onclick":f"ObjectContentControl('{self.objId}', '20')"}
        toRet += self.divStart(atts)
        toRet += self.htmlHead()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Back space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_BS", "class":"ObjectBackSpace", "style":"height:0px;"}
        toRet += self.divStart(atts)
        toRet += self.htmlBack()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Front space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_FS", "class":"ObjectFrontSpace", "style":f"height:{self.height};"}
        toRet += self.divStart(atts)
        toRet += self.htmlFront()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Control space
        #----------------------------------------------------------------------
        atts = {"name":self.objId, "id":f"{self.objId}_CS", "class":"ObjectControlSpace"}
        toRet += self.divStart(atts)
        toRet += self.htmlControll()
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Hidden fields @ Form end
        #----------------------------------------------------------------------
        toRet += str(self.form.hidden_tag())
        self.formStop()
        
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
        # Class specific data
        #----------------------------------------------------------------------
        "This section should be overrided"

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
        "This section should be overrided"

        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlFront(self):
        """"This method should be overrided and return html code
            for the front space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Class specific data
        #----------------------------------------------------------------------
        "This section should be overrided"
            
        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def htmlControll(self):
        """"This method should be overrided and return html code
            for the controll space of this window"""

        toRet = ''

        #----------------------------------------------------------------------
        # Class specific data
        #----------------------------------------------------------------------
        "This section should be overrided"

        #----------------------------------------------------------------------
        return toRet

    
#==============================================================================
print(f"Window {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
