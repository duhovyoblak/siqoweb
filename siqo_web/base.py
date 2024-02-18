#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask                    import url_for, get_flashed_messages, flash, render_template, make_response
from   flask                    import request, session, abort, redirect
from   flask_login              import login_user, logout_user, current_user
from   markupsafe               import escape

import jinja2                   as j2
from   jinja2                   import Environment, PackageLoader, select_autoescape

import siqo_lib.general         as gen

import siqo_web.dms             as dms

from   siqo_web                 import html

from   siqo_web.config          import Config
from   siqo_web.user            import User
from   siqo_web.object          import Object
from   siqo_web.forms           import FormLogin


#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.00'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------


#==============================================================================
# package's methods
#------------------------------------------------------------------------------
def renderItem(item, lang):
    "Returns HTML for json-encoded item"
    
    if 'type' in item.keys(): typ = item['type']
    else                    : typ = 'PARA'
    
    toRet = ''

    #--------------------------------------------------------------------------
    # Rozlisi Backward, Forward alebo nieco ine
    #--------------------------------------------------------------------------
    if False: return toRet

    #--------------------------------------------------------------------------
    # Skusim vsetky zname typy
    #--------------------------------------------------------------------------
    elif typ == 'LINK'         : toRet = html.inputButton(item)
    elif typ == 'CHECKBOX'     : toRet = html.inputCheckBox(item)
    elif typ == 'RADIO'        : toRet = html.inputRadio(item)
    elif typ == 'TEXT'         : toRet = html.inputText(item)

    elif typ == 'LABEL'        : toRet = html.label(item)
    elif typ == 'PARA'         : toRet = html.p(item)
    elif typ == 'P-START'      : toRet = html.pStart(item)
    elif typ == 'P-CONT'       : toRet = html.pCont(item)
    elif typ == 'P-STOP'       : toRet = html.pStop(item)
    elif typ == 'IMAGE'        : toRet = html.image(item)

    elif typ == 'NEWLINE'      : toRet = html.newLine()
    elif typ == 'BREAK'        : toRet = html.breakLine()
    elif typ == 'SPLIT'        : toRet = html.split(item)
    elif typ == 'FUNC'         : toRet = html.fcia(item)
    elif typ == 'HTML'         : toRet = html.html(item)

    elif typ == 'HEADTITLE'    : toRet = html.headTtile(item, lang)
    elif typ == 'HEADSUBTIT'   : toRet = html.headSubTitle(item, lang)
    elif typ == 'HEADCOMMENT'  : toRet = html.headComment(item, lang)

    elif typ == 'BARMENUITEM'  : toRet = html.barMenuItem(item, lang)

    elif typ == 'STAGESELECTOR': toRet = html.stageSelector(item, lang)

    elif typ == 'DIVSTART'     : toRet = html.divStart(item)
    elif typ == 'DIVSTOP'      : toRet = html.divStop(item)
    
    return toRet
    
#==============================================================================
# Base
#------------------------------------------------------------------------------
class Base(Object):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, page, env, height, template="base.html"):
        "Call constructor of Base and initialise it"
        
        journal.I(f"Base({page}).init:")
        
        user = current_user
        
        if user is not None and str(user)[:5]=='User>': 
            
            userId   = user.user_id
            userName = user.userName()
            lang     = user.lang_id
            
        else: 
            userId   = 'Anonymous'
            userName = 'Guest User'
            lang     = 'SK'

        #----------------------------------------------------------------------
        # Konstruktor Database
        #----------------------------------------------------------------------
        super().__init__(journal, page, userId, objPar='__ROOT__', rMode= 'STRICT', crForm='Y', lvl=5)

        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.journal       = journal
        self.loaded        = False
        self.env           = env
        self.userName      = userName
        self.lang          = lang
        self.template      = template
        self.height        = height
        self.initId        = "Content"
        self.context       = {}
        
        #----------------------------------------------------------------------
        # Aktualny user a jazyk
        #----------------------------------------------------------------------
        journal.M(f"Base({self.page}).init: user = '{userName}'")
        journal.M(f"Base({self.page}).init: lang = '{self.lang}'")

        #----------------------------------------------------------------------
        # Inicializacia statickeho contextu
        #----------------------------------------------------------------------
        self.initContext()

        #----------------------------------------------------------------------
        # Doplnenie dynamickeho contextu
        #----------------------------------------------------------------------
        self.pageRes   = self.loadPageResource()
        self.addContext(self.pageRes)

        self.cont   = self.loadContent()
        self.addContext(self.cont)

        #----------------------------------------------------------------------
        # Extra class members
        #----------------------------------------------------------------------
        self.extra  = self.loadExtra()
        self.addContext(self.extra)
        
        self.journal.O(f"Base({self.name}).init")
        
    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadExtra(self):
        
        self.journal.I(f"{self.page}.initExtra:")
        
        self.journal.O()
        return {}
 
    #--------------------------------------------------------------------------
    def loadContent(self):
        
        self.journal.I(f"{self.page}.loadContent:")
        
        self.journal.O()
        return {'content':[{'key':'val'}]}

    #--------------------------------------------------------------------------
    def loadPageResource(self):
        
        self.journal.I(f"{self.page}.loadPageResource:")
        
        res = self.objectGet(self.user)
        toRet = {'heads':{}, 'navs':{}, 'stages':{'sels':{}, 'cnts':{}}}
        
        #----------------------------------------------------------------------
        # Heads items
        #----------------------------------------------------------------------
        if '__HEAD__' in res.keys() and 'res' in res['__HEAD__'].keys():
            
            for key, item in res['__HEAD__']['res'].items():
                
                if   key == 'Title'   : item['type'] = 'HEADTITLE'
                elif key == 'SubTitle': item['type'] = 'HEADSUBTIT'
                elif key == 'Comment' : item['type'] = 'HEADCOMMENT'
        
                toRet['heads'][key] = item

        #----------------------------------------------------------------------
        # NavBar items
        #----------------------------------------------------------------------
        if '__NAVB__' in res.keys() and 'res' in res['__NAVB__'].keys():

            #------------------------------------------------------------------
            # Default polozka v NavBar je User
            #------------------------------------------------------------------
            if 'User' not in res['__NAVB__']['res'].keys():
            
                #--------------------------------------------------------------
                # Polozku 'User' umiestnim na zaciatok dict a doplnim z res['__NAVB__']['res']
                #------------------------------------------------------------------
                dic = {"User":{"type":"BARMENUITEM", "SK":self.userName, "URL":"login"}}
            
                for key, item in res['__NAVB__']['res'].items():
                    
                    item["type"] = "BARMENUITEM"
                    
                    dic[key] = item
            
            #------------------------------------------------------------------
            # Resource s doplnenym 'User' vlozim do Navs
            #------------------------------------------------------------------
            toRet['navs'] = dic
        
        #----------------------------------------------------------------------
        # Stage items
        #----------------------------------------------------------------------
        if '__STAG__' in res.keys() and 'obj' in res['__STAG__'].keys():
            
            for stageId, stage in res['__STAG__']['obj'].items():
    
                pos = stage['res']['StageDef']['POS']
    
                for ncSel, ncRes in stage['obj'].items():
        
                    if ncSel.startswith('SName'):
            
                        for key, item in ncRes['res'].items():
                            
                            item['type'] = 'STAGESELECTOR'
                            item['pos' ] = pos
                            
                            toRet['stages']['sels'][key] = item
                
                    else:
                        for key, item in ncRes['res'].items():

                            item['pos' ] = pos

                            toRet['stages']['cnts'][key] = item

        #----------------------------------------------------------------------
        self.loaded = True
        self.journal.M(f"{self.name}.loadPageResource: {gen.dictString(toRet)}")
        
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
    
    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.page}.respPost: Default None post response")
        
        self.journal.O()
        return None

    #--------------------------------------------------------------------------
    def respGet(self):
     
        self.journal.I(f"{self.page}.respGet: Default html get response from template='{self.template}'")
        
        template = self.env.get_template(self.template)
        self.journal.M(f"{self.name}.resp: template loaded")

        #----------------------------------------------------------------------
        # Vygenerujem html
        #----------------------------------------------------------------------
        resp = make_response(template.render(**self.context), 200)
        resp.headers['X-Something'] = 'A value'

        self.journal.O()
        return resp

    #--------------------------------------------------------------------------
    def resp(self):
     
        self.journal.I(f"{self.page}.resp:")
        
        #----------------------------------------------------------------------
        # Skontrolujem stav stranky, vyskocim ak nie je pripravena
        #----------------------------------------------------------------------
        if not self.loaded:
            self.journal.O()
            abort(500)
        
        #----------------------------------------------------------------------
        # POST Method: Vyhodnotim formulare
        #----------------------------------------------------------------------
        if request.method == 'POST':
            
            resp = self.respPost()
            
            #------------------------------------------------------------------
            # Ak je POST response validna
            #------------------------------------------------------------------
            if resp is not None:
                self.journal.O()
                return resp

        #----------------------------------------------------------------------
        # Default response: Ziskam template a vratim html
        #----------------------------------------------------------------------
        resp = self.respGet()
        self.journal.O()
        return resp

    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    def initContext(self):
        "Creates context"
    
        self.journal.I(f"{self.page}.initContext:")
        self.context = {}

        #----------------------------------------------------------------------
        # Funkcie
        #----------------------------------------------------------------------
        self.context["len"                 ]= len
        self.context["url_for"             ]= url_for
        self.context["get_flashed_messages"]= get_flashed_messages
        self.context["renderItem"          ]= renderItem
        
        #----------------------------------------------------------------------
        # Definicia stranky
        #----------------------------------------------------------------------
        self.context["height"]= self.height
        self.context["initId"]= self.initId
        self.context["lang"  ]= self.lang

        #----------------------------------------------------------------------
        # Navigation Bar
        #----------------------------------------------------------------------
        if str(self.user).startswith("User>"): self.context["userName"]= self.user.userName()
        else                                 : self.context["userName"]= 'Guest User'
        
        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.initContext: Context initialised")
        self.journal.O()

    #--------------------------------------------------------------------------
    def addContext(self, cont):
        "Add optional context"
        
        self.journal.I(f"{self.page}.addContext: {cont.keys()}")
        self.context.update(cont)
        self.journal.O()

    #--------------------------------------------------------------------------
    def addFlash(self, mess):

        self.journal.I(f"{self.page}.addFlash: {mess}")
        flash(mess)
        self.journal.O()

    #--------------------------------------------------------------------------
    def setInitId(self, initId):

        self.journal.I(f"{self.page}.initId: {initId}")
        self.addContext({"initId":initId})
        self.journal.O()

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqo_lib                 import SiqoJournal
    journal = SiqoJournal('test-base', debug=5)
    
    env = Environment(
    
     autoescape = select_autoescape()
    ,loader     = PackageLoader(package_name="siqo_web", package_path="templates")
    )

    page = Base(journal, 'Login', env, 700)
    
#==============================================================================
print(f"Base {_VER}")

"""
for stageId, stage in page.context['__STAG__']['obj'].items():
    
    pos = stage['res']['StageDef']['POS']
    print(stageId, ', pos = ', pos)
    
    for ncSel, res in stage['obj'].items():
        print('--',ncSel)
        
        if ncSel.startswith('SName'):
            
            for key, item in res['res'].items():
                print('-------->', key, '-', item)
                
        else:
            for key, item in res['res'].items():
                print('........>', key, '-', item)
            
"""
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
