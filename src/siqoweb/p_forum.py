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
from   jinja2              import Environment, FileSystemLoader, select_autoescape

import siqolib.general     as gen
from   config              import Config
from   database            import Database
from   app_user            import User
from   app_dms             import DMS
from   p_structure         import Structure

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.01'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Forum
#------------------------------------------------------------------------------
class PageForum(Structure):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, env, classId, link, idx=0, height=700, template="3 forum.html"):
        "Call constructor of Forum and initialise it"
        
        journal.I("PageForum.init:")
        
        #----------------------------------------------------------------------
        # Forum premenne
        #----------------------------------------------------------------------
        self.link = link
        self.idx  = idx

        #----------------------------------------------------------------------
        # Konstruktor Structure
        #----------------------------------------------------------------------
        super().__init__(journal, env, classId=classId, height=height, template=template)
        
        self.journal.O()

    #==========================================================================
    # Content methods
    #--------------------------------------------------------------------------
    def loadContent(self):
        
        self.journal.I(f"{self.name}.loadContent:")
        
        #----------------------------------------------------------------------
        # Nacitanie items
        #----------------------------------------------------------------------
        items = self.loadItem()

        #----------------------------------------------------------------------
        # Nacitanie cache
        #----------------------------------------------------------------------

        #----------------------------------------------------------------------
        self.journal.O()
        return {'__FORUM_ITEM__': {'items':items}}

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
    def readDbItem(self):
    
        self.journal.I(f"{self.name}.readDbItem: {self.idx}")

        #----------------------------------------------------------------------
        # Ak NIE je zname idx nacitam root item fora, inak nacitam nacitam item
        #----------------------------------------------------------------------
        if self.idx > 0: where = f" FORUM_ID = '{self.classId}' and ITEM_ID   = {self.idx}"
        else           : where = f" FORUM_ID = '{self.classId}' and PARENT_ID = 0"

        self.journal.M(f"{self.name}.readDbItem: {where}")
        
        #----------------------------------------------------------------------
        # Nacitanie polozky z DB ako dict
        #----------------------------------------------------------------------
        item = self.readTable(who=self.user, table=Config.tabForum, where=where, header='detail')
        
        #----------------------------------------------------------------------
        self.journal.O()
        return item

    #--------------------------------------------------------------------------
    def loadItem(self):
    
        self.journal.I(f"{self.name}.loadItem: {self.idx}")
        toRet = []

        data = self.readDbItem()
        print(data)
        
        #----------------------------------------------------------------------
        # Kontrola existencie itemu a konverzia hlavicky
        #----------------------------------------------------------------------
        if (type(data) == list) and (len(data)>0): 
            
            title = data[0]['TITLE']
            if data[0]['C_FUNC'] == 'K': title = f"KONCEPT: {title}"
            
            toRet.append( {'TITLE':{'SK': title,                'TYPE':'H2'                  }} )
            toRet.append( {'NARR' :{'SK': data[0]['NARRATOR' ], 'TYPE':'H3'                  }} )
            toRet.append( {'D_CRT':{'SK': data[0]['D_CREATED'], 'TYPE':'DATE'                }} )
            toRet.append( {'D_CHG':{'SK': data[0]['D_CHANGED'], 'TYPE':'DATE'                }} )
            toRet.append( {'TEXT' :{'SK': data[0]['ITEM'     ], 'TYPE':'P', 'link':self.link }} )
            

        else: 
            apology = f"Oops, it seems forum item {self.idx} doesn't exist in forum {self.link}"
            
            toRet.append( {'TITLE':{'SK': apology,      'TYPE':'H2'  }} )
            toRet.append( {'NARR' :{'SK': "Unknown",    'TYPE':'H3'  }} )
            toRet.append( {'D_CRT':{'SK': 'now',        'TYPE':'DATE'}} )
            toRet.append( {'D_CHG':{'SK': 'now',        'TYPE':'DATE'}} )
            toRet.append( {'TEXT' :{'SK': '',           'TYPE':'P'   }} )

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal                 import SiqoJournal
    journal = SiqoJournal('test-base', debug=7)
    
    env = Environment(
     autoescape = select_autoescape()
    ,loader     = FileSystemLoader(['templates'])
    )

    page = PageForum(journal, env, classId='FAQ', idx=275, height=700)
    rec  = page.context

#==============================================================================
print(f"Forum {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
