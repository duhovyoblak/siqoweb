#==============================================================================
#                                             (c) SIQO 11, 12, 13, 24
# Kniznica pre pracu s HTML dokumentom
#
#------------------------------------------------------------------------------
import os
import re

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.01'

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
journal = None
db      = None

#==============================================================================
# Class HTML
#------------------------------------------------------------------------------
class HTML:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, who, dms=None):
        
        self.journal = journal
        self.who     = who
        self.dms     = dms

    #--------------------------------------------------------------------------
    def itemListRender(self, itemLst, lang):
        "Returns HTML for json-encoded item"
        
        toRet = ''
    
        #----------------------------------------------------------------------
        # Prejdem zoznam itemov
        #----------------------------------------------------------------------
        for itemDic in itemLst:
            
            print()
            print('---->', itemDic)
            
            #------------------------------------------------------------------
            # Z itemDic vytiahnem jeho definiciu
            #------------------------------------------------------------------
            item = list(itemDic.values())[0]
            toRet += self.itemRender(item, lang)
            
        print()
        print('<----', toRet)
        return toRet
        
    #--------------------------------------------------------------------------
    def itemRender(self, item, lang):
        "Returns HTML for json-encoded item"
        
        (item, typ) = self.itemDrop(item, 'TYPE')
        if typ == '': typ = 'P'
        
        print()
        print(typ,'->', item)
        
        toRet = ''
    
        #----------------------------------------------------------------------
        # Rozlisi Backward, Forward alebo nieco ine
        #----------------------------------------------------------------------
    
        #----------------------------------------------------------------------
        # Skusim vsetky zname typy
        #----------------------------------------------------------------------
        if   typ == 'CHECKBOX'      : toRet = self.inputCheckBox(item, lang)
    #    elif typ == 'BUTTON'        : toRet = self.inputButton(item, lang)
        elif typ == 'RADIO'         : toRet = self.inputRadio(item, lang)
        elif typ == 'TEXT'          : toRet = self.inputText(item, lang)
    
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
        
        return toRet
        
    #--------------------------------------------------------------------------
    def itemDrop(self, item, key):
        
        if key in item.keys(): 
            
            val = item[key]
            item[key] = ''
            
        else: val = ''
        
        return (item, val)
        
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
        
        (item, txt) = self.itemDrop(item, lang)
    
        return f'<h{deg} {self.html_atts(item)}>{txt}</h1> \n'
    
    #--------------------------------------------------------------------------
    # Link <a href="url"?args>txt</a>
    #--------------------------------------------------------------------------
    def a(self, item, lang):

        print('a')
        print(item)

        (item, url) = self.itemDrop(item, 'URL')
        (item, arg) = self.itemDrop(item, 'ARG')
        (item, txt) = self.itemDrop(item, lang )
    
        link = url
        if arg != '': link += f'?{arg}'
        
        item["href"] = link
        
        print(item)
    
        return f'<a {self.html_atts(item)}>{txt}</a>'
    
    #--------------------------------------------------------------------------
    # Paragraph
    #--------------------------------------------------------------------------
    def pDecode(self, txt, lang):
        
        toRet = txt
        
        #----------------------------------------------------------------------
        # Nahradenie split
        #----------------------------------------------------------------------
        splits = re.findall(r'{SPLIT.*?}', txt)
        
        for spl in splits:
            
            splitHtml = self.split()
            toRet = re.sub(spl, splitHtml, toRet)
        
        #----------------------------------------------------------------------
        # Nahradenie liniek
        #----------------------------------------------------------------------
        links = re.findall(r'{LINK.+?}', txt)
        
        for link in links:
            
            parts = link[1:-1].split(',')
            args  = {'URL':parts[1], lang:parts[2]}
            aHtml = self.a(args, lang)
            
            toRet = re.sub(link, aHtml, toRet)
        
        #----------------------------------------------------------------------
        # Nahradenie obrazkov
        #----------------------------------------------------------------------
        images = re.findall(r'{IMAGE.+?}', txt)
        
        for image in images:
            
            parts = image[1:-1].split(',')
            # {IMAGE,   57,  , 40%, right}
            #        dmsId, h,   w, float
            
            args  = {'sdmId' :parts[1].strip()
                    ,'height':parts[2].strip()
                    ,'width' :parts[3].strip()
                    }
            
            if len(parts)>2: args['height'] = parts[2].strip()
            else           : args['height'] = ''
    
            if len(parts)>3: args['width' ] = parts[3].strip()
            else           : args['width' ] = ''
    
            if len(parts)>4: args['float' ] = parts[4].strip()
            else           : args['float' ] = 'left'

            imageHtml = self.imageThumb(args, lang)
            
            print('imageHtml ', imageHtml)

            toRet = re.sub(image, imageHtml, toRet)
    
        #----------------------------------------------------------------------
        return toRet
        
    #--------------------------------------------------------------------------
    def p(self, item, lang):
        
        toRet  = self.pStart(item, lang)
        toRet += self.pStop()
    
        return toRet
    
    #--------------------------------------------------------------------------
    def pStart(self, item, lang):
    
        (item, hid) = self.itemDrop(item, 'hidden')
        (item, txt) = self.itemDrop(item, lang )
        
        txt = self.pDecode(txt, lang)
    
        #----------------------------------------------------------------------
        # If paragraph is/is not hidden
        #----------------------------------------------------------------------
        if hid == '_none_' or not hid: return f'<p        {self.html_atts(item)}>{txt}'
        else                         : return f'<p hidden {self.html_atts(item)}>{txt}'
    
    #--------------------------------------------------------------------------
    def pCont(self, item, lang):
    
        (item, txt) = self.itemDrop(item, lang )
    
        txt = self.pDecode(txt, lang)
    
        return txt
    
    #--------------------------------------------------------------------------
    def pStop(self, item = {}, lang='SK'):
    
        (item, txt) = self.itemDrop(item, lang )
        
        txt = self.pDecode(txt, lang)
    
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
    
        (item, txt) = self.itemDrop(item, lang)
        return f'<pre {self.html_atts(item)}>{txt}</pre>\n'
    
    #--------------------------------------------------------------------------
    def label(self, item, lang):
    
        (item, txt) = self.itemDrop(item, lang)
        return f'<label {self.html_atts(item)}>{txt}</label>\n'
    
    #==========================================================================
    # Viacriadkove HTML vyrazy
    #--------------------------------------------------------------------------
    def divStart(self, item):
        
        return f'<div {self.html_atts(item)}>\n'
    
    #--------------------------------------------------------------------------
    def divStop(self):
    
        return '</div> \n'
    
    #--------------------------------------------------------------------------
    def divBreak(self, item, lang):
    
        atts = { "class": "Break"}
    
        return f'<div {self.html_atts(atts)}></div> \n'
        
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
    def image(self, item, lang):
        
        return f'<img {self.html_atts(item)}>' 
        
    #--------------------------------------------------------------------------
    def imageThumb(self, item, lang):
     
        #----------------------------------------------------------------------
        # Informacie v iteme
        #----------------------------------------------------------------------
        (item, sdmId ) = self.itemDrop(item, 'sdmId' )
        (item, height) = self.itemDrop(item, 'height')
        (item, width ) = self.itemDrop(item, 'width' )
        (item, flt   ) = self.itemDrop(item, 'float' )
    
        #----------------------------------------------------------------------
        # Informacie ziskane z SDM podla sdmId
        #----------------------------------------------------------------------
        doc  = self.dms.docById(self.who, sdmId)
        
        uri   = doc['URI'  ]
        title = doc['TITLE']

        #----------------------------------------------------------------------
        # Div
        #----------------------------------------------------------------------
        args = {"class"  :"ObjectImage"
               ,"name"   :f"sdm_{sdmId}"
               ,"id"     :f"sdm_{sdmId}"
               ,"style"  :f"height:{height}; width:{width}; float:{flt}"
               }
        toRet = self.divStart(args)
    
        #----------------------------------------------------------------------
        # Link
        #----------------------------------------------------------------------
        args = {"src"    :uri
               ,"style"  :"width:100%; max-height:90%"
               ,"alt"    :"SIQO DMS is loading image..."
               }
    
        linkTxt = self.image(args, lang)
        
        args = {"URL":uri, "target":"_blank", lang:linkTxt}
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
        (item, pos) = self.itemDrop(item, 'pos')
        
        item['name'   ] = 'SSB'
        item['id'     ] = f"SSB_{pos}"
        item['value'  ] = pos
        item['onclick'] = f"ShowStage('{pos}')"
        
        if pos == '1': item['checked'] = True
        else         : item['checked'] = False
    
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
        (item, pos      ) = self.itemDrop(item, 'pos')
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
        (item, pos      ) = self.itemDrop(item, 'pos')
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
        (item, pos      ) = self.itemDrop(item, 'pos')
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
