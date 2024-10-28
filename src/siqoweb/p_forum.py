#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
import os

import flask
from   flask               import url_for, get_flashed_messages, flash, render_template, make_response
from   flask               import request, session, abort, redirect
from   flask_login         import login_user, logout_user, current_user
from   markupsafe          import escape

import jinja2              as j2
from   jinja2              import Environment, PackageLoader, select_autoescape

import siqolib.general     as gen
from   config              import Config
from   database            import Database
from   app_user            import User
from   app_dms             import DMS
from   p_structure         import Structure

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
# Forum
#------------------------------------------------------------------------------
class Forum(Structure):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, env, classId, idx=0, height=700, template="3 forum.html"):
        "Call constructor of Forum and initialise it"
        
        journal.I("Forum.init:")
        
        #----------------------------------------------------------------------
        # Konstruktor Structure
        #----------------------------------------------------------------------
        super().__init__(journal, env, classId=classId, height=height, template=template)
        
        #----------------------------------------------------------------------
        # Forum premenne
        #----------------------------------------------------------------------
        self.idx = idx

        self.journal.O()

    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadContent(self):
        
        self.journal.I(f"{self.name}.loadContent:")
        
        #----------------------------------------------------------------------
        # Nacitanie items
        #----------------------------------------------------------------------
        #items = self.loadItems(self.idx)

        #----------------------------------------------------------------------
        # Nacitanie cache
        #----------------------------------------------------------------------
        cache = {}

        #----------------------------------------------------------------------
        self.journal.O()
        return {'items':'items', 'cache':cache}

    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost:")
        
        #----------------------------------------------------------------------
        # Ak je POST, najprv vyhodnotim formular formLogin
        #----------------------------------------------------------------------
        if self.formLogin.validate_on_submit():
            
            self.journal.M(f"{self.name}.resp: User logged in")
            self.journal.O()
#            return redirect(url_for('orum'))
 
        #----------------------------------------------------------------------
        # Nie je POST
        #----------------------------------------------------------------------
        self.journal.O()
        return None

    #==========================================================================
    # Private methods
    #--------------------------------------------------------------------------
    def loadItem(self, idx):
    
        self.journal.I(f"{self.name}.loadItem: {idx}")

        where = f" FORUM_ID = '{self.classId}' and ITEM_ID = {self.idx}"
        self.journal.M(f"{self.name}.loadItem: {where}")
        
        item = self.readTable(who=self.user, table=Config.tabForum, where=where)
        
        #----------------------------------------------------------------------
        self.journal.O()
        return item

    #--------------------------------------------------------------------------
    def loadItems(self, idx):
    
        self.journal.I(f"{self.name}.loadItem: {idx}")
        toRet = []

        data = self.loadItem(idx)
        
        #----------------------------------------------------------------------
        # Kontrola existencie itemu a konverzia na object
        #----------------------------------------------------------------------
        if (type(data) == list) and (len(data)>0): 
            
            # Titul
            title = data[0]['TITLE']
            if data[0]['C_FUNC'] == 'K': title = f"KONCEPT: {title}"
            
            toRet.append( {'TITLE':{'SK': title,               'TYPE':'H2'}} )
            toRet.append( {'NARR' :{'SK': data[0]['NARRATOR'], 'TYPE':'H3'}} )
            
            
            
        else: 
            toRet.append( {'TITLE':{'SK': f"Forum item id '{idx}' does not exists", 'TYPE':'H2'}} )
            toRet.append( {'NARR' :{'SK': "Unknown",                                'TYPE':'H3'}} )

        #----------------------------------------------------------------------
        self.journal.O()
        print(toRet)
        return toRet

    #--------------------------------------------------------------------------

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

    forum = Forum(journal, env, 57)
    

#==============================================================================
print(f"Forum {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
