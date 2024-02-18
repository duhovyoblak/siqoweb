#==============================================================================
#                                             (c) SIQO 11, 12, 13, 24
# Kniznica pre pracu s HTML dokumentom
#
#------------------------------------------------------------------------------
import os

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
# HTML library
#==============================================================================
# Jednoriadkove HTML vyrazy
#------------------------------------------------------------------------------
def newLine():

    return "\n"

#------------------------------------------------------------------------------
def breakLine():

    return '<br>'

#------------------------------------------------------------------------------
# Headers
#------------------------------------------------------------------------------
def h1(txt, idx =''):

     return f'<h1 {html_attribute("id", idx)}>{html_entities(txt)}</h1> \n'

#------------------------------------------------------------------------------
def h2(txt, idx =''):

    return f'<h2 {html_attribute("id", idx)}>{html_entities(txt)}</h2> \n'

#------------------------------------------------------------------------------
def h3(txt, idx =''):

    return f'<h3 {html_attribute("id", idx)}>{html_entities(txt)}</h3> \n'

#------------------------------------------------------------------------------
def h4(txt, idx =''):

    return f'<h4 {html_attribute("id", idx)}>{html_entities(txt)}</h4> \n'

#------------------------------------------------------------------------------
# Link <a href="url"?args>txt</a>
#------------------------------------------------------------------------------
def a(url, txt, atts={}, args=None):

    link = url
    if args is not None: link += f'?{args}'
    
    atts["href"] = link

    return f'<a {html_atts(atts)}>{html_entities(txt)}</a>'

#------------------------------------------------------------------------------
def p(txt, atts={}, htmlEncoded=True, isHidden=False):

    #--------------------------------------------------------------------------
    # If paragraph is not hidden
    #--------------------------------------------------------------------------
    if not isHidden:
      
        if htmlEncoded:
            return f'<p {html_atts(atts)}>{html_entities(txt)}</p> \n'
           
        else:
            # POZOR, BEZPECNOSTNA DIERA vyriesena cez HTMLSecure !!!
            return f'<p {html_atts(atts)}>{HTMLSecure(txt)}</p> \n'
    
    #--------------------------------------------------------------------------
    # If paragraph is hidden
    #--------------------------------------------------------------------------
    else:
        return f'<p hidden {html_atts(atts)}>{html_entities(txt)}</p> \n'

#------------------------------------------------------------------------------
def pStart(atts={}):

    return f'<p {html_atts(atts)}>'

#------------------------------------------------------------------------------
def pCont(txt):

    return html_entities(txt)

#------------------------------------------------------------------------------
def pStop():

    return '</p>\n'

#------------------------------------------------------------------------------
def split():

    return p('––«•»––', atts={"class":"center"})

#------------------------------------------------------------------------------
def html(code):

    return f'{code} \n'

#------------------------------------------------------------------------------
def pre(txt, atts={}):

    return f'<pre {html_atts(atts)}>{html_entities(txt)}</pre> \n'

#------------------------------------------------------------------------------
def label(txt, idx, atts={}):

    return f'<label for="{idx}" {html_atts(atts)}>{html_entities(txt)}</label> \n'

#==============================================================================
# Viacriadkove HTML vyrazy
#------------------------------------------------------------------------------
def divStart(classx, name='', idx='', h='', w='', t='', l='', onClick='', flt=''):
    
    if name=='': name = classx
    if idx =='': idx  = classx
    
    atts = { "class"  : classx
            ,"name"   : name
            ,"id"     : idx
            ,"onClick": onClick
            ,"style"  : f'height:{h} width:{w} top:{t} left:{l} float:{flt}'
           }

    return f'<div {html_atts(atts)}>\n'

#------------------------------------------------------------------------------
def divStop():

    return '</div> \n'

#------------------------------------------------------------------------------
def divBreak(h='', w=''):

    atts = { "class"  : "Break"
            ,"style"  : f'height:{h} width:{w}'
           }

    return f'<div {html_atts(atts)}></div> \n'

#------------------------------------------------------------------------------
def textThumb(idx, url, title, alt, h='', w='', flt='left'):
 
    toRet = divStart("ObjectText", idx, idx, h, w, '', '', '', flt)

    toRet += a(url, p('lorem ipsum'), atts={"target":"_blank"})
       
    if title != '':
        toRet += p(title, atts={"class":"txt file"})
   
    toRet += divStop()
    
    return toRet

#------------------------------------------------------------------------------
def image(idx, url, title, alt, h='', w='', flt='left'):
 
    toRet = divStart("ObjectImage", idx, idx, h, w, '', '', '', flt)

    atts = {"src":url, "style":"width:100% max-height:90%", "alt":alt}
    txt = f'<img {html_atts(atts)}>'

    toRet += a(url, txt, atts={"target":"_blank"})

    if title != '':
        toRet += p(title, atts={"class":"foto"})
   
    toRet += divStop()
    
    return toRet

#------------------------------------------------------------------------------
# Input items
#------------------------------------------------------------------------------
def inputRadio(item, lang):

    item["type"] = "radio"
    
    #--------------------------------------------------------------------------
    # Radio button
    #--------------------------------------------------------------------------
    if 'checked' in item.keys():
        
        if item['ckecked']: checkType = 'checked'
        else              : checkType = ''
        
        item['checked'] = ''
        
    else: checkType = ''
    
    #--------------------------------------------------------------------------
    # Label
    #--------------------------------------------------------------------------
    txt = item[lang]
    item[lang] = ''
    
    atts = {"for": item['id']}
    
    #--------------------------------------------------------------------------
    # html
    #--------------------------------------------------------------------------
    toRet  = f'<input {html_atts(item)} {checkType}/>\n'
    toRet += f'<label {html_atts(atts)}>{txt}</label><br>'

    return toRet

#------------------------------------------------------------------------------
def inputCheckBox(classx, name, value, idx='', edit=True, onChange='', last=''):

    atts = { "type"    : "checkbox"
            ,"class"   : classx
            ,"name"    : name
            ,"value"   : value
            ,"ID"      : idx
            ,"onchange": onChange
           }
    
    if not edit: editType = 'readonly'
    else       : editType = ''
    
    return f'<input {html_atts(atts)} {editType}/>{last}\n'

#------------------------------------------------------------------------------
def inputText(classx, name, value, idx='', size=10, maxlength=40, edit=True, onChange=''):

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
    
    return f'<input {html_atts(atts)} {editType}/>\n'

#------------------------------------------------------------------------------
# Head block
#------------------------------------------------------------------------------
def headTtile(item, lang):
  
    toRet  = divStart("HeaderTitle", name="HeaderTitle", idx="HeaderTitle")
    toRet += h1(item[lang])
    toRet += divStop()
    
    print('headTitle :', toRet)
    return toRet

#------------------------------------------------------------------------------
def headComment(item, lang):
  
    toRet  = divStart("HeaderComment", name="HeaderComment", idx="HeaderComment")
    toRet += h1(item[lang])
    toRet += divStop()

    return toRet

#------------------------------------------------------------------------------
def headSubTitle(item, lang):
  
    return h4(item[lang])

#------------------------------------------------------------------------------
# NavBar block
#------------------------------------------------------------------------------
def barMenuItem(item, lang):
                                                          # barKey
    toRet  = divStart("BarMenuItem", name="BarMenuItem", idx="BarMenuItem")
    toRet += a(item['URL'], item[lang])
    toRet += divStop()
    
    return toRet

#------------------------------------------------------------------------------
# Stage block
#------------------------------------------------------------------------------
def stageSelector(item, lang):
  
    toRet  = divStart("StageSelectorItem")
    
    pos = item['pos']
    item['pos'] = ''
    
    item['name'   ] = 'SSB'
    item['id'     ] = f"SSB_{pos}"
    item['value'  ] = pos
    item['onclick'] = f"ShowStage('{pos}')"
    
    toRet += inputRadio(item, lang)
    
    toRet += divStop()

    return toRet

#------------------------------------------------------------------------------
# HTML Tabulka
#------------------------------------------------------------------------------
def tableStart(classx, name='', idx='', h=''):

    atts = { "class"  : classx
            ,"name"   : name
            ,"ID"     : idx
            ,"style"  : f'height:{h}'
           }

    return f'<table {html_atts(atts)}>\n'

#------------------------------------------------------------------------------
def tableStop():

    return '</table>\n'

#------------------------------------------------------------------------------
def tableRowStart(classx, name='', idx=''):

    atts = { "class"  : classx
            ,"name"   : name
            ,"ID"     : idx
           }

    return f'<tr {html_atts(atts)}>\n'

#------------------------------------------------------------------------------
def tableRowStop():

    return '</tr>\n'

#------------------------------------------------------------------------------
def tableDataItem(classx, value, title='', idx='', colspan=''):

    atts = { "class"  : classx
            ,"value"  : value
            ,"title"  : title
            ,"ID"     : idx
            ,"colspan": colspan
           }

    return f'<td {html_atts(atts)}>html_entities(value)</td>\n'

#------------------------------------------------------------------------------
def tableCheckItem(name, value, classx='', edit=True, onChange='', idx=''):

    return f'<td>{inputCheckBox(classx, name, value, idx, edit, onChange)}</td>\n'

#------------------------------------------------------------------------------
def tableInputItem(name, value, classx, size, maxlength=40, edit=True, onChange='', idx=''):
    
    return f'<td>{inputText(classx, name, value, idx, size, maxlength, edit, onChange)}</td>\n'

#------------------------------------------------------------------------------
def tableInputHidden(name, value):

    atts = { "type"     : "hidden"
            ,"name"     : name
            ,"value"    : value
           }

    return f'<input {html_atts(atts)}/>\n'

#------------------------------------------------------------------------------
#==============================================================================
# Pomocne metody
#------------------------------------------------------------------------------
# Presmerovanie dokumentu
#------------------------------------------------------------------------------
def html_location(location):
 
    return location
 
#------------------------------------------------------------------------------
def html_baseurl(): 

#  návrat http:#<thiswebsite>/<thisdirectory>
#    return "https:#" . _SERVER['HTTP_HOST'] . dirname(_SERVER['PHP_SELF'])

#  návrat http:#<thiswebsite>
    return "http:# . _SERVER['HTTP_HOST'] . '/'"

#==============================================================================
# Bezpecnostne fcie
#------------------------------------------------------------------------------
def HTMLSecure(txt):

    withoutBreaks           = txt.replace('\n', 'PAGMAN_RESERVED_BREAK')
    HTMLSecureWithoutBreaks = html_entities(withoutBreaks)
    HTMLSecureString        = HTMLSecureWithoutBreaks.replace('PAGMAN_RESERVED_BREAK', '<br>')
    
    return(HTMLSecureString)
  
#------------------------------------------------------------------------------
def html_entities(txt):

    return txt

#------------------------------------------------------------------------------
def html_specialchars(txt):

    return txt

#------------------------------------------------------------------------------
def html_attribute(name, value):

    if value != '': return f' {name} ="{html_specialchars(value)}"'
    else          : return ''

#------------------------------------------------------------------------------
def html_atts(atts):

    toRet = ''

    for key, val in atts.items():
        if val != '': toRet += html_attribute(key, val)
        
    return toRet

#------------------------------------------------------------------------------
# Osetrenie vstupu v stringu vratane odstranenia magic quotes
#------------------------------------------------------------------------------
"""
def str_input( txt )

  if  get_magic_quotes_gpc() )
     txt = stripslashes(str)
      
    return str

#------------------------------------------------------------------------------
# Osetrenie vstupu v poli vratane odstranenia magic quotes
#------------------------------------------------------------------------------
def array_input( arr )

  if  get_magic_quotes_gpc() )
  
    while(i = each(arr)) 
      arr[i[0]] = stripslashes(i[1])
    
      
    return arr

#------------------------------------------------------------------------------
# Debug output na obrazovku
#------------------------------------------------------------------------------
def Debug( stat ) 

    printf( "<p>%s\n</p>\n", stat )
"""
#==============================================================================
print(f"html {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
