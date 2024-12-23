#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

from   flask                 import url_for, get_flashed_messages, flash, make_response
from   flask                 import request, session, abort, redirect
from   flask_login           import login_user, logout_user, current_user
from   markupsafe            import escape

import siqolib.general       as gen

from   o__object             import Object
from   f__form               import FormStruct

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.07'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------


#==============================================================================
# package's methods
#==============================================================================
# Structure
#------------------------------------------------------------------------------
class Structure:
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, dms, title, userId, userName, lang, classId, height):
        "Call constructor of the Structure and initialise it"
        
        journal.I(f"Structure({classId}).init:")
        
        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.journal       = journal
        self.name          = f"Struct({classId})"
        self.dms           = dms
        
        self.title         = title   
        self.userId        = userId   
        self.userName      = userName
        self.lang          = lang
        self.classId       = classId   # OBJECT_ID v pagman db
        self.height        = height
        
        self.loaded        = False

        #----------------------------------------------------------------------
        # Inicializacia default objektov
        #----------------------------------------------------------------------
        self.cont          = {}        # Content of the Page in objects
        
        self.initId        = "Content"
        self.context       = {}
        
        self.loadPage('ja')
        

        #----------------------------------------------------------------------
        # Inicializacia statickeho contextu
        #----------------------------------------------------------------------
        #self.initContext()

        #----------------------------------------------------------------------
        # Doplnenie statickeho contextu z DB
        #----------------------------------------------------------------------
        #self.dbContext = self.loadPageResource()
        #self.addContext(self.dbContext)

        #----------------------------------------------------------------------
        #gen.dictPrint(dct=self.context)
        self.journal.O(f"{self.name}.init")
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Structure"
        
        return f"Structure>{', '.join(self.info())}"

    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the Structure"

        toRet = []
        
        #----------------------------------------------------------------------
        # Prejdem vsetky sekcie Page
        #----------------------------------------------------------------------
        for contId, contObj in self.cont.items():
            
            toRet.append('\n')
            toRet.append(f"Section {contId}>")
            
            toRet.append('\n')
            toRet.append(str(contObj))

        return toRet

    #--------------------------------------------------------------------------
    def urlFor(self, endpoint, filename=None):
        
        toRet = f"url_for({endpoint}, filename={filename})"
        
        try                : toRet = url_for(endpoint, filename=filename)
        except RuntimeError: self.journal.M(f"{self.name}.urlFor: RuntimeError", True)

        return toRet    
        
    #==========================================================================
    # HTML renderer
    #--------------------------------------------------------------------------
    def html(self):
        "This method should be overrided and return html code for this Page"

        self.journal.I("{self.name}.html:")
        toRet = ''
        
        #----------------------------------------------------------------------
        # Document start
        #----------------------------------------------------------------------
        toRet += '<!------------------------------------------------------------------> \n'
        toRet += '<!-- SIQO Web Document start                                      --> \n'
        toRet += '<!------------------------------------------------------------------> \n'
        toRet += '<!DOCTYPE html> \n'
        toRet += '<html> \n'

        #----------------------------------------------------------------------
        # Page header
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Document Header                                       --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<head> \n'
        for cmd in self.htmlHead(): toRet += f"{cmd} \n"
        toRet += '</head> \n'
       
        #----------------------------------------------------------------------
        # Page body start
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Document Body                                         --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<body> \n'

        #----------------------------------------------------------------------
        # JS script before content
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- JS before content                                     --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        for cmd in self.htmlScriptBefore(): toRet += f"{cmd} \n"

        #----------------------------------------------------------------------
        # Header object
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Head object                                           --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<div class="Header" id="Header" onclick="ShowElement(\'Content\')"> \n'
        if self.cont['__HEAD__'] is not None: toRet += self.cont['__HEAD__'].html()
        toRet += '</div> \n'

        #----------------------------------------------------------------------
        # NavBar object
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- NavBar object                                         --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<div class="BarMenu" id="BarMenu"> \n'
        if self.cont['__NAVB__'] is not None: toRet += self.cont['__NAVB__'].html()
        toRet += '</div> \n'

        #----------------------------------------------------------------------
        # Flash
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Flash object                                          --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet +=f'<div class="Flash" id="Flash" style="height:{self.height}px; display:none"> \n'
        toRet += '</div> \n'

        #----------------------------------------------------------------------
        # Content start
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Content start                                         --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet +=f'<div class="Content" id="Content" style="height:{self.height}px; display:block"> \n'

        #----------------------------------------------------------------------
        # Objects of stage
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Stage object                                          --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<div class="StageSelector"> \n'
        if self.cont['__SELS__'] is not None: toRet += self.cont['__SELS__'].html()
        toRet += '\n </div> \n'
        
        toRet += '<!-----------------------------------------------------------> \n'
        if self.cont['__STGS__'] is not None: toRet += self.cont['__STGS__'].html()
        
        #----------------------------------------------------------------------
        # Content stop
        #----------------------------------------------------------------------
        if self.cont['__CONT__'] is not None: toRet += self.cont['__CONT__'].html()
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Content stop                                          --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '</div> \n'

        #----------------------------------------------------------------------
        # Tirage
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- Tirage                                                --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<div class="Tirage" onclick="ShowElement(\'Content\')"> \n'
        for cmd in self.htmlTirage(): toRet += f"{cmd} \n"
        toRet += '</div> \n'
    
        #----------------------------------------------------------------------
        # JS script after content
        #----------------------------------------------------------------------
        toRet += '<!-----------------------------------------------------------> \n'
        toRet += '<!-- JS after content                                      --> \n'
        toRet += '<!-----------------------------------------------------------> \n'
        for cmd in self.htmlScriptAfter(): toRet += f"{cmd} \n"

        #----------------------------------------------------------------------
        # Page body stop
        #----------------------------------------------------------------------
        toRet += '</body> \n'

        #----------------------------------------------------------------------
        # Document stop
        #----------------------------------------------------------------------
        toRet += '</html> \n'
        toRet += '<!------------------------------------------------------------------> \n'
        toRet += '<!-- SIQO Web Document stop                                       --> \n'
        toRet += '<!------------------------------------------------------------------> \n'

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def htmlHead(self):
        "Returns list of commands for HTML page header"
        
        toRet = []

        toRet.append( '<meta   http-equiv="Content-Type"      content="text/html; charset=UTF-8">')
        toRet.append( '<meta   name="META HTTP-EQUIV"         content="NO-CACHE">')
        toRet.append( '<meta   name="author"                  content="Palo4">')
    
        href = self.urlFor('static', filename='css/paragraph.css')
        toRet.append(f'<link   href="{href}" rel="stylesheet" type="text/css">')
        
        href = self.urlFor('static', filename='css/structure.css')
        toRet.append(f'<link   href="{href}" rel="stylesheet" type="text/css">')

        href = self.urlFor('static', filename='css/object.css')
        toRet.append(f'<link   href="{href}" rel="stylesheet" type="text/css">')

        href = self.urlFor('static', filename='js/structure.js')
        toRet.append(f'<script src= "{href}" type="text/javascript"></script>')

        toRet.append( '<title>{self.title}</title>')
        
        return toRet

    #--------------------------------------------------------------------------
    def htmlTirage(self):
        "Returns list of commands for HTML page tirage"
        
        toRet = []

        toRet.append( '<div class="TirageItem" style="width:40%" ></div>')
        
        href = self.urlFor('pgContact')
        toRet.append(f'<div class="TirageItem" id="TI_1"><a href="{href}">Kontakt </a></div>')
    
        href = self.urlFor('pgHomepage')
        toRet.append(f'<div class="TirageItem" id="TI_2"><a href="{href}">Homepage</a></div>')
    
        href = self.urlFor('pgFaq')
        toRet.append(f'<div class="TirageItem" id="TI_3"><a href="{href}">F.A.Q.  </a></div>')

        return toRet

    #--------------------------------------------------------------------------
    def htmlScriptBefore(self):
        "Returns list of commands for HTML page script to be executed before content"
        
        toRet = []

        toRet.append(f'<script>InitElement("{self.initId}")</script>')

        return toRet

    #--------------------------------------------------------------------------
    def htmlScriptAfter(self):
        "Returns list of commands for HTML page script to be executed after content"
        
        toRet = []

        toRet.append('<script>ShowInitElement()</script>')
        toRet.append('<script>ShowStage(1)</script>')

        return toRet

    #==========================================================================
    # Nacitanie page z Database
    #--------------------------------------------------------------------------
#!!!! znacka
    def loadPage(self, who):
        "This method creates all objects for the Page"
        
        self.journal.I(f"{self.name}.pageGet: For page '{self.classId}'")
        
        self.cont = {}

        self.cont['__HEAD__'] = self.getHead(who)
        self.cont['__NAVB__'] = self.getNavb(who)
        
        objSel, objStg = self.getStag(who)
        
        self.cont['__SELS__'] = objSel
        self.cont['__STGS__'] = objStg

        self.cont['__CONT__'] = self.getCont(who)

        self.loaded = True

        #----------------------------------------------------------------------
        self.journal.O()
        return self.cont

    #--------------------------------------------------------------------------
    def getHead(self, who):
        "This method creates Head object and loads for parent __HEAD__ from Database"
        
        self.journal.I(f"{self.name}.getHead:")
        
        objs = Object(self.journal, self.dms, self.userId, self.lang, self.classId, objPar='__HEAD__')
        
        #----------------------------------------------------------------------
        # Skontrolujem, ci existuje prave jeden Head objekt
        #----------------------------------------------------------------------
        if (len(objs.conts)!=1) or (type(objs.conts[0])!=Object):
            
            self.journal.M(f"{self.name}.getHead: Head object is missing or duplicated", True)
            self.journal.O()
            return None

        #----------------------------------------------------------------------
        self.journal.O()
        return objs.conts[0]

    #--------------------------------------------------------------------------
    def getNavb(self, who):
        "This method creates NavBar object and loads for parent __NAVB__ from Database"
        
        self.journal.I(f"{self.name}.getNavb:")
        
        #----------------------------------------------------------------------
        # Nacitam NavBar objekty z Database
        #----------------------------------------------------------------------
        objs = Object(self.journal, self.dms, self.userId, self.lang, self.classId, objPar='__NAVB__')
        
        #----------------------------------------------------------------------
        # Skontrolujem, ci existuje prave jeden NavBar objekt
        #----------------------------------------------------------------------
        if (len(objs.conts)!=1) or (type(objs.conts[0])!=Object):
            self.journal.M(f"{self.name}.getNavb: NavBar object is missing or duplicated", True)
            self.journal.O()
            return None
        
        #----------------------------------------------------------------------
        # NavBar objekt je jediny objekt v objs
        #----------------------------------------------------------------------
        objNavb = objs.conts[0]

        #----------------------------------------------------------------------
        # Na prvu poziciu vlozim link na pgLogin
        #----------------------------------------------------------------------
        objNavb.conts.insert(0, {"SK":self.userName, "URL":"pgLogin"} )

        #----------------------------------------------------------------------
        # Vsetkym itemom nastavim type=BARMENUITEM
        #----------------------------------------------------------------------
        for navItem in objNavb.conts: navItem["TYPE"] = "BARMENUITEM"

        self.journal.O()
        return objNavb

    #--------------------------------------------------------------------------
    def getStag(self, who):
        "This method creates objSel a objStg objects and loads them for parent __STAG__ from Database"
        
        self.journal.I(f"{self.name}.getStag:")

        #----------------------------------------------------------------------
        # Pripravim vysledne objekty SelectorObject a StageObject
        #----------------------------------------------------------------------
        objSel = Object(self.journal, self.dms, self.userId, self.lang, self.classId)
        objStg = Object(self.journal, self.dms, self.userId, self.lang, self.classId)
        
        #----------------------------------------------------------------------
        # Nacitam Stage objekty z Database
        #----------------------------------------------------------------------
        objs = Object(self.journal, self.dms, self.userId, self.lang, self.classId, objPar='__STAG__')
        
        #----------------------------------------------------------------------
        # Skontrolujem, ci tam je aspon jeden Stage objekt
        #----------------------------------------------------------------------
        if (len(objs.conts)==0) or (type(objs.conts[0])!=Object):
            
            self.journal.M(f"{self.name}.getStag: Stage object is missing", True)
            self.journal.O()
            return (objSel, objStg)

        #----------------------------------------------------------------------
        # Prejdem vsetky raw objekty
        #----------------------------------------------------------------------
        for rawObj in objs.conts:
    
            #------------------------------------------------------------------
            # Skontrolujem existenciu selector itemu a aspon jedneho itemu stage conntentu
            #------------------------------------------------------------------
            if len(rawObj.conts) < 2:
                self.journal.M(f"{self.name}.getStag: Stage without any content will be skipped", True)
                continue

            #------------------------------------------------------------------
            # Skontrolujem definiciu pozicie v prvom iteme = Selector item
            #------------------------------------------------------------------
            if 'POS' not in rawObj.conts[0].keys():
                self.journal.M(f"{self.name}.getStag: Stage without 'POS' will be skipped", True)
                continue

            #------------------------------------------------------------------
            # Rozdelim rawObj na objCurSel a objCurStg
            #------------------------------------------------------------------
            objCurSel = Object(self.journal, self.dms, self.userId, self.lang, self.classId)
            objCurSel.contSet(who, contList=[rawObj.conts[0]])

            objCurStg = Object(self.journal, self.dms, self.userId, self.lang, self.classId)
            objCurStg.contSet(who, contList=rawObj.conts[1:])

            #------------------------------------------------------------------
            # Doplnim vlastnosti objCurSel
            #------------------------------------------------------------------
            objCurSel.conts[0]['TYPE'] = 'STAGESELECTOR'
                    
            # Pozicia je v kluci POS ako string, prehodim na int
            stagePos = int(objCurSel.conts[0]['POS'])
            objCurSel.conts[0]['POS'] = stagePos
                    
            #------------------------------------------------------------------
            # Ak objCurStg obsahuje len 1 item
            #------------------------------------------------------------------
            if len(objCurStg.conts) == 1:
                            
                if 'TYPE' in objCurStg.conts[0].keys(): typeStash = objCurStg.conts[0]['TYPE']
                else                                  : typeStash = 'P'
                            
                objCurStg.conts[0]['TYPE'     ] = 'STAGEBOTH'
                objCurStg.conts[0]['typeStash'] = typeStash
                objCurStg.conts[0]['POS'      ] = stagePos
                        
            #------------------------------------------------------------------
            # Ak stage conntent obsahuje viac items
            #------------------------------------------------------------------
            else:
                #--------------------------------------------------------------
                # Prvy item zmenim na typ 'STAGESTART' a pridam POS
                #--------------------------------------------------------------
                if 'TYPE' in objCurStg.conts[0].keys(): typeStash = objCurStg.conts[0]['TYPE']
                else                                  : typeStash = 'P'
                            
                objCurStg.conts[0]['TYPE'     ] = 'STAGESTART'
                objCurStg.conts[0]['typeStash'] = typeStash
                objCurStg.conts[0]['POS'      ] = stagePos

                #--------------------------------------------------------------
                # Posledny item zmenim na typ 'STAGESTOP'
                #--------------------------------------------------------------
                if 'TYPE' in objCurStg.conts[-1].keys(): typeStash = objCurStg.conts[-1]['TYPE']
                else                                   : typeStash = 'P'
                            
                objCurStg.conts[-1]['TYPE'     ] = 'STAGESTOP'
                objCurStg.conts[-1]['typeStash'] = typeStash

            #------------------------------------------------------------------
            # Pridam current objekty do vyslednych objektov
            #------------------------------------------------------------------
            objSel.conts.append(objCurSel)
            objStg.conts.append(objCurStg)
               
        #----------------------------------------------------------------------
        # Zosortujem vysledne objekty objSel a objStg podla POS
        #----------------------------------------------------------------------
        objSel.contSort(who, key='POS')
        objStg.contSort(who, key='POS')
            
        #----------------------------------------------------------------------
        self.journal.O()
        return (objSel, objStg)
    
    #--------------------------------------------------------------------------
    def getCont(self, who):
        "This method creates content objects and loads them for parent __CONT__ from Database"
        
        self.journal.I(f"{self.name}.getCont:")
        toRet = None
        
        
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
        
    #--------------------------------------------------------------------------
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    # Context methods
    #--------------------------------------------------------------------------
    def initContext(self):
        "Creates context"
    
        self.journal.I(f"{self.name}.initContext:")
        self.context = {}

        #----------------------------------------------------------------------
        # Funkcie
        #----------------------------------------------------------------------
        self.context["len"                 ] = len
        self.context["url_for"             ] = url_for
        self.context["get_flashed_messages"] = get_flashed_messages
        self.context["html"                ] = self.html
        
        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.context["height"              ] = self.height
        self.context["initId"              ] = self.initId
        self.context["lang"                ] = self.lang

        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.initContext: Context initialised")
        self.journal.O()

    #--------------------------------------------------------------------------
    def addContext(self, cont):
        "Add optional context"
        
        self.journal.I(f"{self.name}.addContext: {cont.keys()}")
        self.context.update(cont)
        self.journal.O()

    #--------------------------------------------------------------------------
    def addFlash(self, mess):

        self.journal.I(f"{self.name}.addFlash: {mess}")
        flash(mess)
        self.journal.O()

    #--------------------------------------------------------------------------
    def setInitId(self, initId):

        self.journal.I(f"{self.name}.initId: {initId}")
        
        self.initId = initId
        self.addContext({"initId":self.initId})
         
        self.journal.O()

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal       import SiqoJournal
    from   config                import Config
    from   app_dms               import DMS
    
    journal = SiqoJournal('test-Structure', debug=5)
    
    dms = DMS (journal, Config.dtbsName, Config.dtbsPath)
    
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'PagManLogin', 700)
    page = Structure(journal, dms, 'Titul stranky', 'palo4', 'Pavol H', 'SK', 'PagManHomepage', 700)
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'FAQ', 700)
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'OHISTORY', 700)
#    page = Structure(journal, env, 'palo4', 'Pavol H', 'SK', 'PagManContact', 700)
 
    print(page)
    print()
    print(page.html())

#    item = page.dms.loadForumItem('ja', forumId='OHISTORY')

    
#==============================================================================
print(f"Structure {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
