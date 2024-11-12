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
_VER           = '1.02'

_DAY_CHANGES   = 32       # Pocet dni, pocas ktorych sa item povazuje za cerstvo zmeneny
_TITLE_MAX     = 36       # Maximalny pocet zobrazenych znakov TITLE v selectore

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
    def __init__(self, journal, env, classId, target, idx=0, height=700, template="3 forum.html"):
        "Call constructor of Forum and initialise it"
        
        journal.I("PageForum.init:")
        
        #----------------------------------------------------------------------
        # Forum premenne
        #----------------------------------------------------------------------
        self.target    = target          # Nazov route metody pre zvolene forum
        self.idx       = idx           # Cislo itemu, default = 0 pre root
        self.forumItem = None          # Forum item nacitany z DB vo forme dict

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
        toRet = {}
        
        #----------------------------------------------------------------------
        # Nacitanie Forum item
        #----------------------------------------------------------------------
        items = self.loadItem()
        toRet['__FORUM_ITEM__'] = {'items':items}

        #----------------------------------------------------------------------
        # Nacitanie Siblings/Changes
        #----------------------------------------------------------------------
        sibs = self.loadSiblings()
        toRet['__SIBLINGS__'] = {'items':sibs}

        #----------------------------------------------------------------------
        # Nacitanie children
        #----------------------------------------------------------------------
        child = self.loadChildren()
        toRet['__CHILDREN__'] = {'items':child}

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

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
    def loadItem(self):
    
        self.journal.I(f"{self.name}.loadItem: {self.idx}")
        toRet = []

        data = self.readForumItem()
        #print(data)
        
        #----------------------------------------------------------------------
        # Kontrola existencie itemu a konverzia hlavicky
        #----------------------------------------------------------------------
        if (type(data) == dict) and (len(data)>0): 
            
            title = data['TITLE']
            if data['C_FUNC'] == 'K': title = f"KONCEPT: {title}"
            
            toRet.append( {'TITLE':{'SK': title,             'TYPE':'H2'                      }} )
            toRet.append( {'NARR' :{'SK': data['NARRATOR' ], 'TYPE':'H3'                      }} )
            toRet.append( {'D_CRT':{'SK': data['D_CREATED'], 'TYPE':'DATE'                    }} )
            toRet.append( {'D_CHG':{'SK': data['D_CHANGED'], 'TYPE':'DATE'                    }} )
            toRet.append( {'TEXT' :{'SK': data['ITEM'     ], 'TYPE':'TEXT_ITEM', 'target':self.target }} )

        else: 
            apology = f"Oops, it seems forum item {self.idx} doesn't exist in forum {self.target}"
            
            toRet.append( {'TITLE':{'SK': apology          , 'TYPE':'H2'    }} )
            toRet.append( {'NARR' :{'SK': "Unknown"        , 'TYPE':'H3'    }} )
            toRet.append( {'D_CRT':{'SK': 'now'            , 'TYPE':'DATE'  }} )
            toRet.append( {'D_CHG':{'SK': 'now'            , 'TYPE':'DATE'  }} )
            toRet.append( {'TEXT' :{'SK': ''               , 'TYPE':'P'     }} )

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def loadSiblings(self):
    
        self.journal.I(f"{self.name}.loadSiblings: {self.idx}")
        toRet = []

        data = self.readSiblings()
        #print(data)
        
        #----------------------------------------------------------------------
        # Zoznam posledne zmenenych itemov pre root item, inak siblings
        #----------------------------------------------------------------------
        if self.idx == 0: toRet.append( {'SibsLabel':{'SK': 'Naposledy zmenené kapitoly',  'TYPE':'LABEL' }} )
        else            : toRet.append( {'SibsLabel':{'SK': 'Obsah tejto kapitoly'      ,  'TYPE':'LABEL' }} )

        toRet.append( {'SibsSplit':{'TYPE':'SPLIT'}} )
        
        #----------------------------------------------------------------------
        # Konverzia nacitanych riadkov z DB do itemov
        #----------------------------------------------------------------------
        i = 0
        for row in data:

            idx   = str(row[0])
            func  = row[1]
            title = row[2]
            
            #------------------------------------------------------------------
            # Pre koncepty vlozim pred titul C
            #------------------------------------------------------------------
            if func=='K': title = f"C {title}"
        
            toRet.append( {f"sibl_{i}": {'class':'smallFont', 'SK':title[:_TITLE_MAX], 'TYPE':'A', 'URL':self.target, 'IDX':idx, 'BREAK':True }} )

            i += 1
      
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #--------------------------------------------------------------------------
    def loadChildren(self):
    
        self.journal.I(f"{self.name}.loadChildren: {self.idx}")
        toRet = []

        data = self.readChildren()
        #print(data)
        
        #----------------------------------------------------------------------
        # Zoznam posledne zmenenych itemov pre root item, inak siblings
        #----------------------------------------------------------------------
        toRet.append( {'ChildLabel':{'SK': 'Podkapitoly',  'TYPE':'LABEL' }} )
        toRet.append( {'ChildSplit':{'TYPE':'SPLIT'}} )
        
        #----------------------------------------------------------------------
        # Konverzia nacitanych riadkov z DB do itemov
        #----------------------------------------------------------------------
        i = 0
        for row in data:

            idx   = str(row[0])
            func  = row[1]
            title = row[2]
            
            #------------------------------------------------------------------
            # Pre koncepty vlozim pred titul C
            #------------------------------------------------------------------
            if func=='K': title = f"C {title}"
        
            toRet.append( {f"child_{i}": {'class':'smallFont', 'SK':title[:_TITLE_MAX], 'TYPE':'A', 'URL':self.target, 'IDX':idx, 'BREAK':True }} )

            i += 1
      
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet

    #==========================================================================
    # Work with DB
    #--------------------------------------------------------------------------
    def readForumItem(self):
    
        self.journal.I(f"{self.name}.readForumItem: {self.idx}")

        #----------------------------------------------------------------------
        # Ak NIE je zname idx nacitam root item fora, inak nacitam nacitam item
        #----------------------------------------------------------------------
        if self.idx > 0: where = f" FORUM_ID = '{self.classId}' and ITEM_ID   = {self.idx}"
        else           : where = f" FORUM_ID = '{self.classId}' and PARENT_ID = 0"

        self.journal.M(f"{self.name}.readForumItem: {where}")
        
        #----------------------------------------------------------------------
        # Nacitanie polozky z DB ako dict
        #----------------------------------------------------------------------
        item = self.readTable(who=self.user, table=Config.tabForum, where=where, header='detail')
        self.forumItem = item[0]
        
        #----------------------------------------------------------------------
        self.journal.O()
        return self.forumItem

    #--------------------------------------------------------------------------
    def readSiblings(self):
        "Reads from DB items with the same PARENT_ID, e.g. siblings or last changed items in case of the root item"
    
        self.journal.I(f"{self.name}.readSiblings: {self.idx}")

        #----------------------------------------------------------------------
        # Kontrola existencie itemu
        #----------------------------------------------------------------------
        if self.forumItem is None:
            
            self.journal.M(f"{self.name}.readSiblings: Forum item idx={self.idx} does not exist, command denied")
            self.journal.O()
            return []

        #----------------------------------------------------------------------
        # Zoznam posledne zmenenych itemov pre root item, inak siblings
        #----------------------------------------------------------------------
        if self.idx == 0: where = f" FORUM_ID = '{self.classId}' and julianday('now')-julianday(d_changed) <= {_DAY_CHANGES}"
        else            : where = f" FORUM_ID = '{self.classId}' and PARENT_ID = {self.forumItem['PARENT_ID']}"
    
        self.journal.M(f"{self.name}.readSiblings: {where}")
        
        #----------------------------------------------------------------------
        # Nacitanie zoznamu TITLEs z DB ako list
        #----------------------------------------------------------------------
        sql = f"select ITEM_ID, C_FUNC, TITLE from {Config.tabForum} where {where}"
        sibs = self.readDb(who=self.user, sql=sql)
        
        #----------------------------------------------------------------------
        self.journal.O()
        return sibs

    #--------------------------------------------------------------------------
    def readChildren(self):
        "Reads from DB items which have PARENT_ID the same as my ID, e.g. children items"
    
        self.journal.I(f"{self.name}.readChildren: {self.idx}")

        #----------------------------------------------------------------------
        # Kontrola existencie itemu
        #----------------------------------------------------------------------
        if self.forumItem is None:
            
            self.journal.M(f"{self.name}.readChildren: Forum item idx={self.idx} does not exist, command denied")
            self.journal.O()
            return []

        #----------------------------------------------------------------------
        # Nacitanie zoznamu TITLEs z DB ako list
        #----------------------------------------------------------------------
        sql = f"select ITEM_ID, C_FUNC, TITLE from {Config.tabForum} where FORUM_ID = '{self.classId}' and PARENT_ID = {self.forumItem['ITEM_ID']}"
        child = self.readDb(who=self.user, sql=sql)
        
        #----------------------------------------------------------------------
        self.journal.O()
        return child

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

    page = PageForum(journal, env, classId='FAQ', target='pgFaq', idx=275, height=700)
    rec  = page.context

#==============================================================================
print(f"Forum {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
