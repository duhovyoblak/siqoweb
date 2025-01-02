#==============================================================================
#                                             (c) SIQO 11, 12, 13, 24
# Kniznica pre pracu s HTML dokumentom
#
#------------------------------------------------------------------------------
import os
import re
import traceback

from   datetime              import date
from   flask                 import url_for, redirect

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER           = '1.14'

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
    def __init__(self, journal, userId, lang, classId='noClass'):
        
        self.journal   = journal
        self.name      = f"HTML_{userId}"
        self.userId    = userId   
        self.lang      = lang
        self.classId   = classId   # OBJECT_ID v pagman db
        
    #--------------------------------------------------------------------------
    def urlFor(self, url):
        
        toRet = f"url_for('{url}')"

        #----------------------------------------------------------------------
        # Null response
        #----------------------------------------------------------------------
        if url.strip()=='': return ""
        
        #----------------------------------------------------------------------
        # Page response
        #----------------------------------------------------------------------
        try                : toRet = url_for(url)
        except RuntimeError: self.journal.M(f"{self.name}.urlFor: RuntimeError", True)

        return toRet    
        
    #--------------------------------------------------------------------------
    def toLogin(self):
     
        return redirect(self.urlFor('pgLogin'))

    #--------------------------------------------------------------------------
    def toHomepage(self):
     
        return redirect(self.urlFor('pgHomepage'))

    #--------------------------------------------------------------------------
    def itemDrop(self, item, key, pop=False):
        
        if key in item.keys(): 
            
            if pop: val = item.pop(key)
            else  : val = item[key]
            
        else: val = ''
        
        return (item, val)
        
    #--------------------------------------------------------------------------
    def itemTxt(self, item):
        
        (item, txt) = self.itemDrop(item, self.lang, pop=True)
        
        return (item, txt)
        
    #==========================================================================
    # Rendering API for templates
    #--------------------------------------------------------------------------
    def objectsRender(self, objDic):
        "Returns HTML for json-encoded item"
        
        self.journal.I(f"{self.name}.objectsRender: Going to render an object dictionary...")
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
                toRet += self.objectsRender(rec)
                
            #------------------------------------------------------------------
            # Ak je rec typu list, ide o zoznam itemov
            #------------------------------------------------------------------
            elif type(rec)==list:
              
                #--------------------------------------------------------------
                # Zavolam itemListRender
                #--------------------------------------------------------------
                toRet += self.itemListRender(rec, objId)
            
            #------------------------------------------------------------------
            # Inak je to neznamy udaj
            #------------------------------------------------------------------
            else:
                self.journal.M(f"{self.name}.objectsRender: UNKNOWN object '{objDic}'", True)

        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
        
    #--------------------------------------------------------------------------
    def itemListRender(self, itemLst, objId='noObjId'):
        "Returns HTML for json-encoded item"
        
        self.journal.I(f"{self.name}.itemListRender: Going to render a list of items...")
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
                toRet += self.itemRender(itemDic, objId)
            
        self.journal.O()
        return toRet
        
    #--------------------------------------------------------------------------
#!!!!
    def itemRender(self, item, objId='noObjId'):
        "Returns HTML for json-encoded item"
        
        self.journal.I(f"{self.name}.itemRender: I will render item {objId} for lang = '{self.lang}'")
        toRet = ''

        #----------------------------------------------------------------------
        # Priprava
        #----------------------------------------------------------------------
        try:
            #item['objId'] = f"{self.classId}.{objId}"
            copyItem = dict(item)
        
            (item, typ) = self.itemDrop(item, 'TYPE', pop=True)
            if typ == '': typ = 'P'

        except Exception as err:
            
            self.journal.M(f"{self.name}.itemRender: {str(err)}", True)
            self.journal.O()
            return f'<p>{str(err)}</p><br><p>{item}</p>'

        #----------------------------------------------------------------------
        self.journal.M(f"{self.name}.itemRender: {typ} for def {item}")

        #----------------------------------------------------------------------
        # Skusim vsetky zname typy
        #----------------------------------------------------------------------
        try:
            if   typ == 'CHECKBOX'      : toRet = self.inputCheckBox(item  )
            elif typ == 'RADIO'         : toRet = self.inputRadio(item     )
            elif typ == 'BUTTON'        : toRet = self.inputButton(item    )
            elif typ == 'TEXT'          : toRet = self.inputText(item      )
            
            elif typ == 'LABEL'         : toRet = self.label(item)
            elif typ == 'H1'            : toRet = self.h(item,  1)
            elif typ == 'H2'            : toRet = self.h(item,  2)
            elif typ == 'H3'            : toRet = self.h(item,  3)
            elif typ == 'H4'            : toRet = self.h(item,  4)
            elif typ == 'P'             : toRet = self.p(item    )
            elif typ == 'P_START'       : toRet = self.pStart(item )
            elif typ == 'P_CONT'        : toRet = self.pCont(item  )
            elif typ == 'P_STOP'        : toRet = self.pStop(item  )
            elif typ == 'A'             : toRet = self.a(item      )
            elif typ == 'IMAGE'         : toRet = self.image(item  )
            elif typ == 'DATE'          : toRet = self.datePar(item)
            elif typ == 'TEXT_ITEM'     : toRet = self.textItem(item)
    
            elif typ == 'HEADTITLE'     : toRet = self.headTtile(item   )
            elif typ == 'HEADSUBTIT'    : toRet = self.headSubTitle(item)
            elif typ == 'HEADCOMMENT'   : toRet = self.headComment(item )
    
            elif typ == 'BARMENUITEM'   : toRet = self.barMenuItem(item )
    
            elif typ == 'STAGESELECTOR' : toRet = self.stageSelector(item)
            elif typ == 'STAGEBOTH'     : toRet = self.stageBoth(item   )
            elif typ == 'STAGESTART'    : toRet = self.stageStart(item  )
            elif typ == 'STAGESTOP'     : toRet = self.stageStop(item   )
    
            elif typ == 'NEWLINE'       : toRet = self.newLine()
            elif typ == 'BREAK'         : toRet = self.breakLine()
            elif typ == 'SPLIT'         : toRet = self.split()
        
            elif typ == 'FUNC'          : toRet = self.ftion(item)
            elif typ == 'HTML'          : toRet = self.html(item)
            elif typ == 'DIVSTART'      : toRet = self.divStart(item)
            elif typ == 'DIVSTOP'       : toRet = self.divStop()
            
        #----------------------------------------------------------------------
        # Error handling
        #----------------------------------------------------------------------
        except Exception as err:
            
            self.journal.M(f"{self.name}.itemRender: {str(err)}", True)
            self.journal.O()
            return f'<p>{str(err)}</p><br><p>{copyItem}</p><br><p>{traceback.format_exc()}</p>'
        
        #----------------------------------------------------------------------
        self.journal.O()
        return toRet
        
    #==========================================================================
    # Private htm rendering methods
    #--------------------------------------------------------------------------
    def newLine(self, ):
    
        return "\n"
    
    #--------------------------------------------------------------------------
    def breakLine(self, ):
    
        return '<br>'
    
    #--------------------------------------------------------------------------
    # Headers
    #--------------------------------------------------------------------------
    def h(self, item, deg):
        
        (item, txt) = self.itemTxt(item)
    
        return f'<h{deg} {self.html_atts(item)}>{txt}</h1> \n'
    
    #--------------------------------------------------------------------------
    # Link <a href="url"/idx=idx?args>txt</a>
    #--------------------------------------------------------------------------
    def a(self, item):

        (item, uri) = self.itemDrop(item, 'URI'  )
        (item, url) = self.itemDrop(item, 'URL'  )
        (item, idx) = self.itemDrop(item, 'IDX'  )
        (item, arg) = self.itemDrop(item, 'ARG'  )
        (item, brk) = self.itemDrop(item, 'BREAK')
        
        (item, txt) = self.itemTxt(item)
    
        #----------------------------------------------------------------------
        # Vytvorenie href - prednost ma uri
        #----------------------------------------------------------------------
        if uri != '': 
            link = uri
            
        else:
            link = self.urlFor(url)
            if idx != '': link += f'/{idx.strip()}'
            if arg != '': link += f'?{arg}'
        
        item["href"] = link

        #----------------------------------------------------------------------
        toRet = f'<a {self.html_atts(item)}>{txt}</a>'
        if brk: toRet += self.breakLine()
        
        self.journal.M(f"{self.name}.a:{toRet}")
        return toRet
    
    #--------------------------------------------------------------------------
    # Paragraph
    #--------------------------------------------------------------------------
    def p(self, item):
        
        toRet  = self.pStart(item)
        toRet += self.pStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def pStart(self, item={}):
    
        
        (item, txt   ) = self.itemTxt (item)
        (item, hid   ) = self.itemDrop(item, 'hidden')

        #----------------------------------------------------------------------
        # If paragraph is/is not hidden
        #----------------------------------------------------------------------
        if hid == '_none_' or not hid: return f'<p {self.html_atts(item)}>{txt}'
        else                         : return f'<p hidden {self.html_atts(item)}>{txt}'
    
    #--------------------------------------------------------------------------
    def pCont(self, item={}):
    
        (item, txt   ) = self.itemTxt(item)
    
        return txt
    
    #--------------------------------------------------------------------------
    def pStop(self, item={}):
    
        (item, txt   ) = self.itemTxt(item)
        
        return f'{txt}</p>\n'
    
    #--------------------------------------------------------------------------
    def split(self, ):
    
        atts = {"SK":"––«•»––", "class":"center"}
        return self.p(atts)
    
    #--------------------------------------------------------------------------
    def html(self, item):
    
        (item, code) = self.itemDrop(item, 'html')
        return f'{code}\n'
    
    #--------------------------------------------------------------------------
    def ftion(self, item):
    
        (item, ftion) = self.itemDrop(item, 'func')
        return f'{ftion}\n'
    
    #--------------------------------------------------------------------------
    def pre(self, item):
    
        (item, txt) = self.itemTxt(item)
        return f'<pre {self.html_atts(item)}>{txt}</pre>\n'
    
    #--------------------------------------------------------------------------
    def label(self, item):
    
        (item, txt) = self.itemTxt(item)
        return f'<label {self.html_atts(item)}>{txt}</label>\n'
    
    #--------------------------------------------------------------------------
    # Text item
    #--------------------------------------------------------------------------
    def textItem(self, item):

        (item, txt   ) = self.itemTxt(item)
        (item, target) = self.itemDrop(item, 'target')

        self.journal.I(f"{self.name}.textItem: {txt[:32]}...")

        #----------------------------------------------------------------------
        # Vlozenie zdrojoveho textu
        #----------------------------------------------------------------------
        toRet  = self.pStart( {self.lang:txt} )
        toRet += self.pStop()

        #----------------------------------------------------------------------
        # Nahradenie split
        #----------------------------------------------------------------------
        splits = re.findall(r'{\s*SPLIT\s*}', txt)
        
        for spl in splits:
            
            self.journal.M(f"{self.name}.textItem: SPLIT {spl}")

            repl  = self.pStop() + self.split() + self.pStart()
            toRet = re.sub(spl, repl, toRet)
        
        #----------------------------------------------------------------------
        # Nahradenie liniek
        #----------------------------------------------------------------------
        links = re.findall(r'{\s*LINK.+?}', txt)
        
        for link in links:
            
            self.journal.M(f"{self.name}.textItem: LINK {link}")

            parts = link[1:-1].split(',')
            
            idx  = parts[1]
            aTxt = parts[2]
            
            args  = {'URL':target, 'IDX':idx, self.lang:aTxt}

            repl  = self.a(args)
            toRet = re.sub(link, repl, toRet)
        
        #----------------------------------------------------------------------
        # Nahradenie obrazkov
        #----------------------------------------------------------------------
        images = re.findall(r'{\s*IMAGE.+?}', txt)

        for image in images:
            
            self.journal.M(f"{self.name}.textItem: IMAGE {image}")

            parts = image[1:-1].split(',')
            # {IMAGE,  idx,  h, w, float}
            
            args  = {'idx'   :parts[1].strip() }
            
            if len(parts)>2: args['height'] = parts[2].strip()
            else           : args['height'] = ''
    
            if len(parts)>3: args['width' ] = parts[3].strip()
            else           : args['width' ] = ''
    
            if len(parts)>4: args['float' ] = parts[4].strip()
            else           : args['float' ] = 'left'

            repl  = self.pStop() + self.imageThumb(args) + self.pStart()
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
    def textThumb(self, item):
     
    #    toRet = divStart("ObjectText", idx, idx, h, w, '', '', '', flt)
        toRet = self.divStart(item)
    
    #    toRet += a(url, p('lorem ipsum'), atts={"target":"_blank"})
           
    #    if title != '':
    #        toRet += p(title, atts={"class":"txt file"})
       
        toRet += self.divStop()
        
        return toRet
    
    #--------------------------------------------------------------------------
    def datePar(self, item):
        
        (item, dat) = self.itemTxt(item)
        
        day = date.fromisoformat(dat[:10]) 
        
        item[self.lang] = day.strftime('%d.%m. %Y')

        return self.p(item)
        
    #--------------------------------------------------------------------------
    def image(self, item):
        
        return f'<img {self.html_atts(item)}>' 
        
    #--------------------------------------------------------------------------
    def imageThumb(self, item):
     
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
        doc  = self.dms.docById(self.userId, idx)
        
        uri   = doc['URI'  ]
        title = doc['TITLE']

        args = {"src"    :uri
               ,"style"  :"width:100%; max-height:90%"
               ,"alt"    :"SIQO DMS is loading image..."
               }
    
        linkTxt = self.image(args)
       
        args = {"URI":uri, "target":"_blank", self.lang:linkTxt}
        toRet += self.a(args)
        
        #----------------------------------------------------------------------
        # Titul
        #----------------------------------------------------------------------
        args = {"class":"foto", self.lang:title}
        toRet += self.p(args)
    
        #----------------------------------------------------------------------
        # Div Stop
        #----------------------------------------------------------------------
        toRet += self.divStop()
        
        self.journal.M(f"{self.name}.imageThumb: {toRet}")
        return toRet
    
    #--------------------------------------------------------------------------
    # Input items
    #--------------------------------------------------------------------------
    def inputCheckBox(self, item):
    
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
    def inputRadio(self, item):
    
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
        txt = item[self.lang]
        item[self.lang] = ''
        
        atts = {"for": item['id']}

        #----------------------------------------------------------------------
        # html
        #----------------------------------------------------------------------
        toRet  = f'<input {self.html_atts(item)} {checkType}/>\n'
        toRet += f'<label {self.html_atts(atts)}>{txt}</label><br>'
    
        return toRet
    
    #--------------------------------------------------------------------------
    def inputButton(self, item, enabled=True):

        atts = { "type"       : "text"
                ,"name"       : name
                ,"value"      : value
                ,"class"      : classx
                ,"title"      : title
                ,"formaction" : fact
                ,"onclick"    : onclick
                ,"ID"         : idx
                ,"size"       : size
                ,"maxlength"  : maxlength
                ,"onchange"   : onChange
                ,"formtarget" : target
                ,"style"      : 'width:'
               }
       
        if enabled: return f'<input {self.html_atts(item)} disabled />\n'

    #--------------------------------------------------------------------------
    def inputText(self, item):
    
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
    # Head block
    #--------------------------------------------------------------------------
    def headTtile(self, item):
      
        atts = {"class":"HeaderTitle", "name":"HeaderTitle", "id":"HeaderTitle"}
     
        toRet  = self.divStart(atts)
        toRet += self.h(item, 1)
        toRet += self.divStop()
        
        return toRet
    
    #--------------------------------------------------------------------------
    def headComment(self, item):
      
        atts = {"class":"HeaderComment", "name":"HeaderComment", "id":"HeaderComment"}
    
        toRet  = self.divStart(atts)
        toRet += self.p(item)
        toRet += self.divStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def headSubTitle(self, item):
      
        return self.h(item, 4)
    
    #--------------------------------------------------------------------------
    # NavBar block
    #--------------------------------------------------------------------------
    def barMenuItem(self, item):
        
        atts = {"class":"BarMenuItem", "name":"BarMenuItem", "id":"BarMenuItem"}
        
        toRet  = self.divStart(atts)
        toRet += self.a(item)
        toRet += self.divStop()
        
        return toRet
    
    #--------------------------------------------------------------------------
    # Stage block
    #--------------------------------------------------------------------------
    def stageSelector(self, item):
      
        #----------------------------------------------------------------------
        # Pripravim atributy do itemu
        #----------------------------------------------------------------------
        (item, pos) = self.itemDrop(item, 'POS', True)
        
        item['name'   ] = 'SSB'
        item['id'     ] = f"SSB_{pos}"
        item['onclick'] = f"ShowStage('{pos}')"
        
        if pos == 1: item['checked'] = 'checked'
    
        atts = {"class":"StageSelectorItem", "name":"StageSelectorItem", "id":"StageSelectorItem"}
            
        #----------------------------------------------------------------------
        # Render itemu
        #----------------------------------------------------------------------
        toRet  = self.divStart(atts)
        toRet += self.inputRadio(item)
        toRet += self.divStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def stageBoth(self, item):
      
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
        toRet += self.itemRender(item)
        toRet += self.divStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def stageStart(self, item):
    
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
        toRet += self.itemRender(item)
    
        return toRet
    
    #--------------------------------------------------------------------------
    def stageStop(self, item):
    
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
        toRet  = self.itemRender(item)
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
