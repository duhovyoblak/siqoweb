#==============================================================================
#                                             (c) SIQO 11, 12, 13, 24
# Kniznica pre pracu s HTML dokumentom
#
#------------------------------------------------------------------------------
import os
import re
import traceback
from   flask                    import url_for

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.07'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
#journal = None
#db      = None

#==============================================================================
# Class HTML
#------------------------------------------------------------------------------
class HTML:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, who, dms=None, classId='noClass'):
        
        self.journal = journal
        self.who     = who   
        self.dms     = dms       # DMS manager
        self.classId = classId   # OBJECT_ID v pagman db
        
        #----------------------------------------------------------------------
        # Dynamicky prenasane parametre
        #----------------------------------------------------------------------
        self.idx     = 0

    #--------------------------------------------------------------------------
    def objectsRender(self, objDic, lang):
        "Returns HTML for json-encoded item"
        
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
        return toRet
        
    #--------------------------------------------------------------------------
    def itemListRender(self, itemLst, lang, objId='noObjId'):
        "Returns HTML for json-encoded item"
        
        toRet = ''
    
        #----------------------------------------------------------------------
        # Prejdem zoznam itemov [ {itemId : {arg1:, arg2:, } } ]
        #----------------------------------------------------------------------
        for item in itemLst:
            
            #------------------------------------------------------------------
            # Ziskam itemId a itemDic
            #------------------------------------------------------------------
            for itemId, itemDic in item.items():

                #--------------------------------------------------------------
                # Zavolam itemRender pre itemDic
                #--------------------------------------------------------------
                toRet += self.itemRender(itemDic, lang, objId)
            
        return toRet
        
    #--------------------------------------------------------------------------
    def itemRender(self, item, lang, objId='noObjId'):
        "Returns HTML for json-encoded item"
        
        self.journal.I(f"HTML_{self.who}.itemRender: for lang = '{lang}'")
        toRet = ''

        #----------------------------------------------------------------------
        # Priprava
        #----------------------------------------------------------------------
        try:
            item['objId'] = f"{self.classId}.{objId}"
            copyItem = dict(item)
        
            (item, typ) = self.itemDrop(item, 'TYPE')
            if typ == '': typ = 'P'

        except Exception as err:
            
            self.journal.M(f"HTML_{self.who}.itemRender: {str(err)}", True)
            return f'<p>{str(err)}</p><br><p>{item}</p>'

        #----------------------------------------------------------------------
        # Skusim vsetky zname typy
        #----------------------------------------------------------------------
        try:
            if   typ == 'CHECKBOX'      : toRet = self.inputCheckBox(item, lang)
        #   elif typ == 'BUTTON'        : toRet = self.inputButton(item, lang)
            elif typ == 'RADIO'         : toRet = self.inputRadio(item, lang)
            elif typ == 'TEXT'          : toRet = self.inputText(item, lang)
            
            elif typ == 'OBJECT'        : toRet = self.dbObject(item, lang)

            elif typ == 'LABEL'         : toRet = self.label(item, lang)
            elif typ == 'H1'            : toRet = self.h(item, lang, 1)
            elif typ == 'H2'            : toRet = self.h(item, lang, 2)
            elif typ == 'H3'            : toRet = self.h(item, lang, 3)
            elif typ == 'H4'            : toRet = self.h(item, lang, 4)
            elif typ == 'P'             : toRet = self.p(item, lang)
            elif typ == 'P_START'       : toRet = self.pStart(item, lang)
            elif typ == 'P_CONT'        : toRet = self.pCont(item, lang)
            elif typ == 'P_STOP'        : toRet = self.pStop(item, lang)
            elif typ == 'A'             : toRet = self.a(item, lang)
            elif typ == 'IMAGE'         : toRet = self.image(item, lang)
            elif typ == 'DATE'          : toRet = self.date(item, lang)
            elif typ == 'TEXT_ITEM'     : toRet = self.textItem(item, lang)
    
            elif typ == 'HEADTITLE'     : toRet = self.headTtile(item, lang)
            elif typ == 'HEADSUBTIT'    : toRet = self.headSubTitle(item, lang)
            elif typ == 'HEADCOMMENT'   : toRet = self.headComment(item, lang)
    
            elif typ == 'BARMENUITEM'   : toRet = self.barMenuItem(item, lang)
    
            elif typ == 'STAGESELECTOR' : toRet = self.stageSelector(item, lang)
            elif typ == 'STAGEBOTH'     : toRet = self.stageBoth(item, lang)
            elif typ == 'STAGESTART'    : toRet = self.stageStart(item, lang)
            elif typ == 'STAGESTOP'     : toRet = self.stageStop(item, lang)
    
            elif typ == 'NEWLINE'       : toRet = self.newLine()
            elif typ == 'BREAK'         : toRet = self.breakLine()
            elif typ == 'SPLIT'         : toRet = self.split()
        
            elif typ == 'FUNC'          : toRet = self.ftion(item)
            elif typ == 'HTML'          : toRet = self.html(item)
            elif typ == 'DIVSTART'      : toRet = self.divStart(item)
            elif typ == 'DIVSTOP'       : toRet = self.divStop(item)
            
        #----------------------------------------------------------------------
        # Error handling
        #----------------------------------------------------------------------
        except Exception as err:
            
            self.journal.M(f"HTML_{self.who}.itemRender: {str(err)}", True)
            toRet = f'<p>{str(err)}</p><br><p>{copyItem}</p><br><p>{traceback.format_exc()}</p>'
        
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
        
    #--------------------------------------------------------------------------
    def itemDrop(self, item, key, pop=True):
        
        if key in item.keys(): 
            
            if pop: val = item.pop(key)
            else  : val = item[key]
            
        else: val = ''
        
        return (item, val)
        
    #--------------------------------------------------------------------------
    def itemTxt(self, item, lang):
        
        (item, txt) = self.itemDrop(item, lang)
        
        #if txt == '': txt = f"No resource for lang='{lang}'"
        
        return (item, txt)
        
    #==========================================================================
    # Jednoriadkove HTML vyrazy
    #--------------------------------------------------------------------------
    def newLine(self, ):
    
        return "\n"
    
    #--------------------------------------------------------------------------
    def breakLine(self, ):
    
        return '<br>'
    
    #--------------------------------------------------------------------------
    # Headers
    #--------------------------------------------------------------------------
    def h(self, item, lang, deg):
        
        (item, txt) = self.itemTxt(item, lang)
    
        return f'<h{deg} {self.html_atts(item)}>{txt}</h1> \n'
    
    #--------------------------------------------------------------------------
    # Link <a href="url"/idx=idx?args>txt</a>
    #--------------------------------------------------------------------------
    def a(self, item, lang):

        (item, uri) = self.itemDrop(item, 'URI'  )
        (item, url) = self.itemDrop(item, 'URL'  )
        (item, idx) = self.itemDrop(item, 'IDX'  )
        (item, arg) = self.itemDrop(item, 'ARG'  )
        (item, brk) = self.itemDrop(item, 'BREAK')
        
        (item, txt) = self.itemTxt(item, lang   )
    
        #----------------------------------------------------------------------
        # Vytvorenie href - prednost ma uri
        #----------------------------------------------------------------------
        if uri != '': 
            link = uri
            
        else:
            link = url_for(url)
            if idx != '': link += f'/{idx.strip()}'
            if arg != '': link += f'?{arg}'
        
        item["href"] = link

        #----------------------------------------------------------------------
        toRet = f'<a {self.html_atts(item)}>{txt}</a>'
        if brk: toRet += self.breakLine()
        
        self.journal.M(f"HTML_{self.who}.a:{toRet}")
        return toRet
    
    #--------------------------------------------------------------------------
    # Paragraph
    #--------------------------------------------------------------------------
    def p(self, item, lang):
        
        toRet  = self.pStart(item, lang)
        toRet += self.pStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def pStart(self, item={}, lang='SK'):
    
        
        (item, txt   ) = self.itemTxt (item, lang    )
        (item, hid   ) = self.itemDrop(item, 'hidden')

        #----------------------------------------------------------------------
        # If paragraph is/is not hidden
        #----------------------------------------------------------------------
        if hid == '_none_' or not hid: return f'<p        {self.html_atts(item)}>{txt}'
        else                         : return f'<p hidden {self.html_atts(item)}>{txt}'
    
    #--------------------------------------------------------------------------
    def pCont(self, item={}, lang='SK'):
    
        (item, txt   ) = self.itemTxt(item, lang    )
    
        return txt
    
    #--------------------------------------------------------------------------
    def pStop(self, item={}, lang='SK'):
    
        (item, txt   ) = self.itemTxt(item, lang    )
        
        return f'{txt}</p>\n'
    
    #--------------------------------------------------------------------------
    def split(self, ):
    
        atts = {"SK":"––«•»––", "class":"center"}
        return self.p(atts, 'SK')
    
    #--------------------------------------------------------------------------
    def html(self, item, lang):
    
        (item, code) = self.itemDrop(item, 'html')
        return f'{code}\n'
    
    #--------------------------------------------------------------------------
    def ftion(self, item, lang):
    
        (item, ftion) = self.itemDrop(item, 'func')
        return f'{ftion}\n'
    
    #--------------------------------------------------------------------------
    def pre(self, item, lang):
    
        (item, txt) = self.itemTxt(item, lang)
        return f'<pre {self.html_atts(item)}>{txt}</pre>\n'
    
    #--------------------------------------------------------------------------
    def label(self, item, lang):
    
        (item, txt) = self.itemTxt(item, lang)
        return f'<label {self.html_atts(item)}>{txt}</label>\n'
    
    #--------------------------------------------------------------------------
    # Text item
    #--------------------------------------------------------------------------
    def textItem(self, item, lang):

        (item, txt   ) = self.itemTxt(item, lang)
        (item, target) = self.itemDrop(item, 'target')

        self.journal.I(f"HTML_{self.who}.textItem: {txt[:32]}...")

        args   = {lang:txt}
        toRet  = self.pStart(args, lang)
        toRet += self.pStop()

        #----------------------------------------------------------------------
        # Nahradenie split
        #----------------------------------------------------------------------
        splits = re.findall(r'{\s*SPLIT\s*}', txt)
        
        for spl in splits:
            
            self.journal.M(f"HTML_{self.who}.textItem: SPLIT {spl}")

            repl  = self.pStop() + self.split() + self.pStart()
            toRet = re.sub(spl, repl, toRet)
        
        #----------------------------------------------------------------------
        # Nahradenie liniek
        #----------------------------------------------------------------------
        links = re.findall(r'{\s*LINK.+?}', txt)
        
        for link in links:
            
            self.journal.M(f"HTML_{self.who}.textItem: LINK {link}")

            parts = link[1:-1].split(',')
            
            idx  = parts[1]
            aTxt = parts[2]
            
            args  = {'URL':target, 'IDX':idx, lang:aTxt}

            repl  = self.a(args, lang)
            toRet = re.sub(link, repl, toRet)
        
        #----------------------------------------------------------------------
        # Nahradenie obrazkov
        #----------------------------------------------------------------------
        images = re.findall(r'{\s*IMAGE.+?}', txt)

        for image in images:
            
            self.journal.M(f"HTML_{self.who}.textItem: IMAGE {image}")

            parts = image[1:-1].split(',')
            # {IMAGE,  idx,  h, w, float}
            
            args  = {'idx'   :parts[1].strip() }
            
            if len(parts)>2: args['height'] = parts[2].strip()
            else           : args['height'] = ''
    
            if len(parts)>3: args['width' ] = parts[3].strip()
            else           : args['width' ] = ''
    
            if len(parts)>4: args['float' ] = parts[4].strip()
            else           : args['float' ] = 'left'

            repl  = self.pStop() + self.imageThumb(args, lang) + self.pStart()
            toRet = re.sub(image, repl, toRet)
        
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
        
    #==========================================================================
    # Viacriadkove HTML vyrazy
    #--------------------------------------------------------------------------
    def divStart(self, item):
        
        return f'<div {self.html_atts(item)}>\n'
    
    #--------------------------------------------------------------------------
    def divStop(self):
    
        return '</div> \n'
    
    #--------------------------------------------------------------------------
    def divBreak(self, item):
    
        atts = { "class": "Break"}
    
        return f'<div {self.html_atts(atts)}></div> \n'
        
    #--------------------------------------------------------------------------
    def formStart(self, item):

        return f"<form {self.html_atts(item)}>\n"

    #--------------------------------------------------------------------------
    def formStop(self):
        
        return "</form> \n"
        
    #--------------------------------------------------------------------------
    def textThumb(self, item, lang):
     
    #    toRet = divStart("ObjectText", idx, idx, h, w, '', '', '', flt)
        toRet = self.divStart(item)
    
    #    toRet += a(url, p('lorem ipsum'), atts={"target":"_blank"})
           
    #    if title != '':
    #        toRet += p(title, atts={"class":"txt file"})
       
        toRet += self.divStop()
        
        return toRet
    
    #--------------------------------------------------------------------------
    def date(self, item, lang):
        
        (item, date) = self.itemDrop(item, lang)

        return date 
        
    #--------------------------------------------------------------------------
    def image(self, item, lang):
        
        return f'<img {self.html_atts(item)}>' 
        
    #--------------------------------------------------------------------------
    def imageThumb(self, item, lang):
     
        #----------------------------------------------------------------------
        # Informacie v iteme
        #----------------------------------------------------------------------
        (item, idx   ) = self.itemDrop(item, 'idx'   )
        (item, height) = self.itemDrop(item, 'height')
        (item, width ) = self.itemDrop(item, 'width' )
        (item, flt   ) = self.itemDrop(item, 'float' )

        #----------------------------------------------------------------------
        # Div
        #----------------------------------------------------------------------
        args = {"class"  :"ObjectImage"
               ,"name"   :f"dms_{idx}"
               ,"id"     :f"dms_{idx}"
               ,"style"  :f"height:{height}; width:{width}; float:{flt}"
               }
        toRet = self.divStart(args)
    
        #----------------------------------------------------------------------
        # Link
        #----------------------------------------------------------------------
        doc  = self.dms.docById(self.who, idx)
        
        uri   = doc['URI'  ]
        title = doc['TITLE']

        args = {"src"    :uri
               ,"style"  :"width:100%; max-height:90%"
               ,"alt"    :"SIQO DMS is loading image..."
               }
    
        linkTxt = self.image(args, lang)
       
        args = {"URI":uri, "target":"_blank", lang:linkTxt}
        toRet += self.a(args, lang)
        
        #----------------------------------------------------------------------
        # Titul
        #----------------------------------------------------------------------
        args = {"class":"foto", lang:title}
        toRet += self.p(args, lang)
    
        #----------------------------------------------------------------------
        # Div Stop
        #----------------------------------------------------------------------
        toRet += self.divStop()
        
        self.journal.M(f"HTML_{self.who}.imageThumb: {toRet}")
        return toRet
    
    #--------------------------------------------------------------------------
    # Input items
    #--------------------------------------------------------------------------
    def inputRadio(self, item, lang):
    
        item["type"] = "radio"
        
        #----------------------------------------------------------------------
        # Radio button
        #----------------------------------------------------------------------
        if 'checked' in item.keys():
            
            if item['checked']: checkType = 'checked'
            else              : checkType = ''
            
            item['checked'] = ''
        
        else: checkType = ''
        
        #----------------------------------------------------------------------
        # Label
        #----------------------------------------------------------------------
        txt = item[lang]
        item[lang] = ''
        
        atts = {"for": item['id']}
        
        #----------------------------------------------------------------------
        # html
        #----------------------------------------------------------------------
        toRet  = f'<input {self.html_atts(item)} {checkType}/>\n'
        toRet += f'<label {self.html_atts(atts)}>{txt}</label><br>'
    
        return toRet
    
    #--------------------------------------------------------------------------
    def inputCheckBox(self, item, lang):
    
        """
        atts = { "type"    : "checkbox"
                ,"class"   : classx
                ,"name"    : name
                ,"value"   : value
                ,"ID"      : idx
                ,"onchange": onChange
               }
        
        if not edit: editType = 'readonly'
        else       : editType = ""
        """
        editType = ''
        return f'<input {self.html_atts(item)} {editType}/>\n'
    
    #--------------------------------------------------------------------------
    def inputText(self, item, lang):
    
        """
        atts = { "type"     : "text"
                ,"class"    : classx
                ,"name"     : name
                ,"value"    : value
                ,"ID"       : idx
                ,"size"     : size
                ,"maxlength": maxlength
                ,"onchange" : onChange
               }
        
        if not edit: editType = 'readonly'
        else       : editType = ''
        """
        editType = ''
        return f'<input {self.html_atts(item)} {editType}/>\n'
    
    #--------------------------------------------------------------------------
    # DB Objects block
    #--------------------------------------------------------------------------
#!!!!
    def dbObject(self, item, lang):
        """Renders objects based on parameters"""
        
        toRet = ''
        
        #----------------------------------------------------------------------
        # Define parameters of an object
        #----------------------------------------------------------------------
        (item, objClass    ) = self.itemDrop(item, 'CLASS' )
        (item, target      ) = self.itemDrop(item, 'target', False)
        (item, crForm      ) = self.itemDrop(item, 'crForm')
        
        (item, objId       ) = self.itemDrop(item, 'objId' )
        (item, height      ) = self.itemDrop(item, 'height')
        (item, width       ) = self.itemDrop(item, 'width' )
        
        if width  == '': width  = '99%'
        if height == '': height = '94%'
  
        #----------------------------------------------------------------------
        # Read instance of the object for respective class
        #----------------------------------------------------------------------
        dbItem = self.loadDbItem(who='ja', objClass=objClass, item=item)
        
        if len(dbItem) == 0:
            
            self.journal.M(f"HTML_{self.who}.dbObject: No dbItem for class={objClass} and item={item}", True)
            return toRet

        #----------------------------------------------------------------------
        # Render the object formular
        #----------------------------------------------------------------------
        if crForm == 'Y': 
            
            method = 'POST'
            action = url_for(target)
    
            atts = {"name":objId, "id":objId, "method":method, "action":action, "enctype":"multipart/form-data"}
            toRet += self.formStart(atts)

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
        
#         ShowBack( $stage, $action );
        
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
        
#           $this->ShowButtons();
        
        toRet += self.divStop()

        #----------------------------------------------------------------------
        # Object space end
        #----------------------------------------------------------------------
        toRet += self.divStop()

        #----------------------------------------------------------------------
        if crForm == 'Y': self.formStop()
        
        #----------------------------------------------------------------------
        return toRet

    #--------------------------------------------------------------------------
    def loadDbItem(self, who, objClass, item):
        
        toRet = {}
    
        #----------------------------------------------------------------------
        # Nacitanie objektu podla class
        #----------------------------------------------------------------------
        if objClass == 'FORUM':
            
            (item, forumId) = self.itemDrop(item, 'FORUM', False)
            
            toRet = self.dms.loadForumItem(who, forumId=forumId, idx=self.idx, target='')
            
       
        #----------------------------------------------------------------------
        print('dbItem > ', toRet)
        return toRet
    
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
    def objectFront(self, objClass, item, dbItem, lang):

        toRet = ''

        #----------------------------------------------------------------------
        # Vytvorenie Front/end objektu podla class
        #----------------------------------------------------------------------
        if objClass == 'FORUM':
            
            (dbItem, objId) = self.itemDrop(dbItem, 'ITEM_ID'  )
            (dbItem, parId) = self.itemDrop(dbItem, 'PARENT_ID')
            (dbItem, narr ) = self.itemDrop(dbItem, 'NARR'     )
            (dbItem, d_crt) = self.itemDrop(dbItem, 'D_CRT'    )
            (dbItem, d_chg) = self.itemDrop(dbItem, 'D_CHG'    )
            (dbItem, text ) = self.itemDrop(dbItem, 'TEXT'     )
            
            (item, forumId) = self.itemDrop(item, 'FORUM' , False)
            (item, target ) = self.itemDrop(item, 'target', False)
            
            idx    = objId['SK']
            parIdx = parId['SK']

            print('idx,    ', idx)
            print('parIdx, ', parIdx)
            
            
            
            #------------------------------------------------------------------
            # Vykreslenie Siblings/Changes
            #------------------------------------------------------------------
            toRet += self.divStart({"class":"Selector", "style":"height:100%; width:20%; display:block"})
            sibs   = self.dms.loadForumSiblings(who='ja', forumId=forumId, parIdx=parIdx, target=target)
            toRet += self.itemListRender(sibs, lang)
            toRet += self.divStop()
            
            #------------------------------------------------------------------
            # Vykreslenie Vykreslenie Forum itemu
            #------------------------------------------------------------------
            toRet += self.divStart({"class":"ForumItem", "style":"height:100%; width:60%; display:block"})
            toRet += self.itemRender(d_chg, lang)
            toRet += self.itemRender(narr,  lang)
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
    # Head block
    #--------------------------------------------------------------------------
    def headTtile(self, item, lang):
      
        atts = {"class":"HeaderTitle", "name":"HeaderTitle", "id":"HeaderTitle"}
     
        toRet  = self.divStart(atts)
        toRet += self.h(item, lang, 1)
        toRet += self.divStop()
        
        return toRet
    
    #--------------------------------------------------------------------------
    def headComment(self, item, lang):
      
        atts = {"class":"HeaderComment", "name":"HeaderComment", "id":"HeaderComment"}
    
        toRet  = self.divStart(atts)
        toRet += self.p(item, lang)
        toRet += self.divStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def headSubTitle(self, item, lang):
      
        return self.h(item, lang, 4)
    
    #--------------------------------------------------------------------------
    # NavBar block
    #--------------------------------------------------------------------------
    def barMenuItem(self, item, lang):
        
        atts = {"class":"BarMenuItem", "name":"BarMenuItem", "id":"BarMenuItem"}
        
        toRet  = self.divStart(atts)
        toRet += self.a(item, lang)
        toRet += self.divStop()
        
        return toRet
    
    #--------------------------------------------------------------------------
    # Stage block
    #--------------------------------------------------------------------------
    def stageSelector(self, item, lang):
      
        #----------------------------------------------------------------------
        # Pripravim atributy do itemu
        #----------------------------------------------------------------------
        (item, pos) = self.itemDrop(item, 'POS')
        
        item['name'   ] = 'SSB'
        item['id'     ] = f"SSB_{pos}"
        item['value'  ] = pos
        item['onclick'] = f"ShowStage('{pos}')"
        
        if pos == 1: item['checked'] = 'checked'
    
        atts = {"class":"StageSelectorItem", "name":"StageSelectorItem", "id":"StageSelectorItem"}
            
        #----------------------------------------------------------------------
        # Render itemu
        #----------------------------------------------------------------------
        toRet  = self.divStart(atts)
        toRet += self.inputRadio(item, lang)
        toRet += self.divStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def stageBoth(self, item, lang):
      
        #----------------------------------------------------------------------
        # Pripravim atributy do itemu
        #----------------------------------------------------------------------
        (item, pos      ) = self.itemDrop(item, 'POS')
        (item, typeStash) = self.itemDrop(item, 'typeStash')
        
        item['TYPE'   ] = typeStash
        item['name'   ] = 'SContent'
        
        if pos == '1': style = "display:block"
        else         : style = "display:none"
        
        atts = {"class":"StagePanel", "name":"SP", "id":f"SP_{pos}", "style":style}
    
        #----------------------------------------------------------------------
        # Render itemu
        #----------------------------------------------------------------------
        toRet  = self.divStart(atts)
        toRet += self.itemRender(item, lang)
        toRet += self.divStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def stageStart(self, item, lang):
    
        #----------------------------------------------------------------------
        # Pripravim atributy do itemu
        #----------------------------------------------------------------------
        (item, pos      ) = self.itemDrop(item, 'POS')
        (item, typeStash) = self.itemDrop(item, 'typeStash')
        
        item['TYPE'   ] = typeStash
        item['name'   ] = 'SContent'
        
        if pos == '1': style = "display:block"
        else         : style = "display:none"
        
        atts = {"class":"StagePanel", "name":"SP", "id":f"SP_{pos}", "style":style}
    
        #----------------------------------------------------------------------
        # Render itemu
        #----------------------------------------------------------------------
        toRet  = self.divStart(atts)
        toRet += self.itemRender(item, lang)
    
        return toRet
    
    #--------------------------------------------------------------------------
    def stageStop(self, item, lang):
    
        #----------------------------------------------------------------------
        # Pripravim atributy do itemu
        #----------------------------------------------------------------------
        (item, pos      ) = self.itemDrop(item, 'POS')
        (item, typeStash) = self.itemDrop(item, 'typeStash')
        
        item['TYPE'   ] = typeStash
        item['name'   ] = 'SContent'
        
        #----------------------------------------------------------------------
        # Render itemu
        #----------------------------------------------------------------------
        toRet  = self.itemRender(item, lang)
        toRet += self.divStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    # HTML Tabulka
    #--------------------------------------------------------------------------
    def tableStart(self, classx, name='', idx='', h=''):
    
        atts = { "class"  : classx
                ,"name"   : name
                ,"ID"     : idx
                ,"style"  : f'height:{h}'
               }
    
        return f'<table {self.html_atts(atts)}>\n'
    
    #--------------------------------------------------------------------------
    def tableStop(self):
    
        return '</table>\n'
    
    #--------------------------------------------------------------------------
    def tableRowStart(self, classx, name='', idx=''):
    
        atts = { "class"  : classx
                ,"name"   : name
                ,"ID"     : idx
               }
    
        return f'<tr {self.html_atts(atts)}>\n'
    
    #--------------------------------------------------------------------------
    def tableRowStop(self):
    
        return '</tr>\n'
    
    #--------------------------------------------------------------------------
    def tableDataItem(self, classx, value, title='', idx='', colspan=''):
    
        atts = { "class"  : classx
                ,"value"  : value
                ,"title"  : title
                ,"ID"     : idx
                ,"colspan": colspan
               }
    
        return f'<td {self.html_atts(atts)}>html_entities(value)</td>\n'
    
    #--------------------------------------------------------------------------
    def tableCheckItem(self, name, value, classx='', edit=True, onChange='', idx=''):
    
        return f'<td>{self.inputCheckBox(classx, name, value, idx, edit, onChange)}</td>\n'
    
    #--------------------------------------------------------------------------
    def tableInputItem(self, name, value, classx, size, maxlength=40, edit=True, onChange='', idx=''):
        
        return f'<td>{self.inputText(classx, name, value, idx, size, maxlength, edit, onChange)}</td>\n'
    
    #--------------------------------------------------------------------------
    def tableInputHidden(self, name, value):
    
        atts = { "type"     : "hidden"
                ,"name"     : name
                ,"value"    : value
               }
    
        return f'<input {self.html_atts(atts)}/>\n'
    
    #--------------------------------------------------------------------------
    #==========================================================================
    # Pomocne metody
    #--------------------------------------------------------------------------
    # Presmerovanie dokumentu
    #--------------------------------------------------------------------------
    def html_location(self, location):
     
        return location
     
    #--------------------------------------------------------------------------
    def html_baseurl(self): 
        
        #  návrat http:#<thiswebsite>/<thisdirectory>
        #    return "https:#" . _SERVER['HTTP_HOST'] . dirname(_SERVER['PHP_SELF'])
        
    #  návrat http:#<thiswebsite>
        return "http:# . _SERVER['HTTP_HOST'] . '/'"
    
    #==========================================================================
    # Bezpecnostne fcie
    #--------------------------------------------------------------------------
    def HTMLSecure(self, txt):
    
        withoutBreaks           = txt.replace('\n', 'PAGMAN_RESERVED_BREAK')
        HTMLSecureWithoutBreaks = self.html_entities(withoutBreaks)
        HTMLSecureString        = HTMLSecureWithoutBreaks.replace('PAGMAN_RESERVED_BREAK', '<br>')
        
        return(HTMLSecureString)
      
    #--------------------------------------------------------------------------
    def html_entities(self, txt):
    
        return txt
    
    #--------------------------------------------------------------------------
    def html_specialchars(self, txt):
    
        return txt
    
    #--------------------------------------------------------------------------
    def html_attribute(self, name, value):
    
        if value != '': return f' {name} ="{self.html_specialchars(value)}"'
        else          : return ''
    
    #--------------------------------------------------------------------------
    def html_atts(self, atts):
    
        toRet = ''
    
        for key, val in atts.items():
            if val != '': toRet += self.html_attribute(key, val)
            
        return toRet
    
    #--------------------------------------------------------------------------
    # Osetrenie vstupu v stringu vratane odstranenia magic quotes
    #--------------------------------------------------------------------------
    """
    def str_input( txt )
    
      if  get_magic_quotes_gpc() )
         txt = stripslashes(str)
          
        return str
    
    #--------------------------------------------------------------------------
    # Osetrenie vstupu v poli vratane odstranenia magic quotes
    #--------------------------------------------------------------------------
    def array_input( arr )
    
      if  get_magic_quotes_gpc() )
      
        while(i = each(arr)) 
          arr[i[0]] = stripslashes(i[1])
        
          
        return arr
    
    #--------------------------------------------------------------------------
    # Debug output na obrazovku
    #--------------------------------------------------------------------------
    def Debug( stat ) 
    
        printf( "<p>%s\n</p>\n", stat )
    """
#==============================================================================
print(f"html {_VER}")
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
