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
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, dms, userId, lang, item, idx=0, height=20, width=20):

        journal.I(f"Window.__init__: for {userId}")

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
        self.idx       = idx                      # Primarny kluc objektu
        
        self.itemDef   = item                     # Item dict definition from DB
        self.dbData    = None                     # Data content from DMS/Formular
        self.dbItem    = None                     # Item content from DMS
        
        self.formPost  = None                     # Data from POST request.form
        self.form      = None                     # Formular asociated with this window
        self.formId    = f"WindowForm_{self.idx}" # Id of the formular
       
        #----------------------------------------------------------------------
        # Nacitanie formulara s POST udajmi
        #----------------------------------------------------------------------
        self.loadForm()

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
        # Vytvorenie window formulara z post data
        #----------------------------------------------------------------------
        "This section should be overrided"

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
        "This section should be overrided"
      
        #----------------------------------------------------------------------
        return (self.dbData, self.dbItem)
    
    #--------------------------------------------------------------------------
    def dbSave(self):
        """"This method should be overrided and save dbData 
            into DMS/Database"""
        
        #----------------------------------------------------------------------
        # Zapis objektu podla class/objId/idx
        #----------------------------------------------------------------------
        "This section should be overrided"
       
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
