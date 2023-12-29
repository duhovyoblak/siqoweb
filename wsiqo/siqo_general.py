#==============================================================================
# Siqo general library
#------------------------------------------------------------------------------
import os
import pickle
import json
import re
import base64

#import pandas        as pd
from   datetime        import date

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

#==============================================================================
# package's variables
#------------------------------------------------------------------------------


#==============================================================================
# Bracket structure Tools
#------------------------------------------------------------------------------
def structDelOuts(struct):
    
    toRet = []
    
    #--------------------------------------------------------------------------
    # Akumulujem polozky vo svojej urovni vnorenia
    #--------------------------------------------------------------------------
    toRet.extend(struct['del-'])
    
    #--------------------------------------------------------------------------
    # Akumulujem polozky v najblizsej nizsej urovni vnorenia
    #--------------------------------------------------------------------------
    for subStruct in struct['sub']:
        
        toRet.extend( structDelOuts(subStruct) )
    
    #--------------------------------------------------------------------------
    return toRet
    
#------------------------------------------------------------------------------
def braDelOuts(txt, bra='(', ket=')', delims=',', totPos=0):
    
    #--------------------------------------------------------------------------
    # Ziskam strukturu txt
    #--------------------------------------------------------------------------
    struct = braSplit(txt, bra, ket, delims, totPos)
    toRet  = structDelOuts(struct)
    
    return toRet
    
#------------------------------------------------------------------------------
def braSplit(txt, bra='(', ket=')', delims=',', totPos=0):
    
#    print(f'SIQO.braSplit: {txt}')
    
    toRet = {}
    toRet['res' ] = 'OK'             # Vysledny stav analyzy
    toRet['txt' ] = txt              # Vstupny text
    toRet['bra' ] = totPos-1         # Pozicia bra v texte nadradenej urovne
    toRet['ket' ] = totPos+len(txt)  # Pozicia ket v texte nadradenej urovne
    
    toRet['del+'] = []               # List delimited casti txt vratane vnoreneho textu
    toRet['del-'] = []               # List delimited casti txt bez vnoreneho textu
    toRet['sub' ] = []               # List vysledkov analyzy vnorenej urovne - rekurzia
    
    pos    = 0                       # Lokalna pozicia spracovavaneho znaku
    depth  = 0                       # Lokalna hlbka vnorenia do 'bra'-'ket'
    acc    = ''                      # Akumulovany text medzi 'bra'-'ket' najvyssej urovne
    cutAll = ''                      # Akumulovany text medzi 'delim' vratane vnoreneho textu
    cutOut = ''                      # Akumulovany text medzi 'delim' bez vnoreneho textu
    
    #--------------------------------------------------------------------------
    # Preskenujem txt po jednom znaku
    #--------------------------------------------------------------------------
    for char in txt:
        
        cutAll += char
        
        #----------------------------------------------------------------------
        # Vyriesim zmenu depth
        #----------------------------------------------------------------------
        if   char == bra: depth  += 1
        elif char == ket: depth  -= 1

        #----------------------------------------------------------------------
        # Ak som vnoreny, akumulujem acc string
        #----------------------------------------------------------------------
        if depth > 0: 
            
            # Ak som sa prave vnoril, tak nastavim startovaciu poziciu vnorenia
            if acc == '': startPos = totPos
            acc += char
            
            # Vnoreny text nepatri medzi delimited casti cutOut
            cutOut = ''
            
        #----------------------------------------------------------------------
        # Skontrolujem ci su bra-ket vybalancovane
        #----------------------------------------------------------------------
        elif depth < 0: 
        
            toRet['res'] = 'ER'
            toRet['txt'] = f'ERROR: extra {ket} at position {pos}'
            return toRet
        
        #----------------------------------------------------------------------
        # Som vynoreny, vyriesim acc string
        #----------------------------------------------------------------------
        else:
            
            #------------------------------------------------------------------
            # Ak bol naakumulovany acc string
            #------------------------------------------------------------------
            if acc != '':
                
                subTxt    = acc[1:]
                subStruct = braSplit(subTxt, bra, ket, delims, startPos+1)
                
                toRet['sub' ].append(subStruct)
                
                if toRet['sub'][-1]['res'] != 'OK': return toRet
                else                              : acc = ''

            #------------------------------------------------------------------
            # Ak som narazil na delimiter
            #------------------------------------------------------------------
            if char in delims:
                
                toRet['del+'].append(cutAll[:-1])
                cutAll = ''

                if cutOut.strip() != '': toRet['del-'].append(cutOut.strip())
                cutOut = ''
            
            else:  
                if char not in [bra, ket]: cutOut += char

        #----------------------------------------------------------------------
        # Prejdem na nasledujuci znak
        #----------------------------------------------------------------------
        pos    += 1
        totPos += 1
        
    #--------------------------------------------------------------------------
    # Skontrolujem ci su bra-ket vybalancovane
    #--------------------------------------------------------------------------
    if depth > 0: 
        
        toRet['res'] = 'ER'
        toRet['txt'] = f'ERROR: {ket} expected but missing'
        return toRet

    #--------------------------------------------------------------------------
    # Doplnim posledny cut
    #--------------------------------------------------------------------------
    toRet['del+'].append(cutAll)
    if cutOut.strip() != '': toRet['del-'].append(cutOut.strip())

    #--------------------------------------------------------------------------
    return toRet        

#------------------------------------------------------------------------------
def aliasSplit(txt):
    
    txt = txt.strip()
    txt = shrink(txt)
    
    #--------------------------------------------------------------------------
    # Zistim ci txt obsahuje ' AS ' 
    #--------------------------------------------------------------------------
    rx = txt.split(' AS ')
            
    #--------------------------------------------------------------------------
    # Neobsahuje ' AS '
    #--------------------------------------------------------------------------
    if len(rx) == 1:
                
        #----------------------------------------------------------------------
        # Zistim ci txt obsahuje ' ', t.j. alias
        #----------------------------------------------------------------------
        sx = txt.split(' ')
                
        #----------------------------------------------------------------------
        # Neobsahuje alias
        #----------------------------------------------------------------------
        if len(sx) == 1:
            stat = sx[0].strip()
            alis = None
                    
        #----------------------------------------------------------------------
        # Obsahuje alias
        #----------------------------------------------------------------------
        else:
            stat = ' '.join(sx[0:-1]).strip()
            alis = sx[-1].strip()
                
    #--------------------------------------------------------------------------
    # Obsahuje ' AS '
    #--------------------------------------------------------------------------
    else:
        stat = ' '.join(rx[0:-1]).strip()
        alis = rx[-1].strip()
                
    #--------------------------------------------------------------------------
    return (stat, alis)

#------------------------------------------------------------------------------
def shrink(txt, toShrink=' '):
    
    toRet = txt
    
    #--------------------------------------------------------------------------
    # Ziskam vsetky suvisle vyskyty toShrink texte a zmenim na jeden toShrink
    #--------------------------------------------------------------------------
    ss = toShrink + '{2,}'
      
    if re.search(ss, txt): toRet = re.sub(ss, toShrink, txt)
    
    #--------------------------------------------------------------------------
    return toRet
        
#==============================================================================
# String value tests
#------------------------------------------------------------------------------
def isNumber(s):
    
    rx = re.findall(r'[^\d.-]', s)
    if len(rx) > 0: return False
    
    try:
        float(s)
        return True
    
    except ValueError:
        return False
    
#------------------------------------------------------------------------------
def isRc(item):
    
    s = re.sub(r'[ .\-/]', '', item)
    if (len(s)<9) or (len(s)>10): return 0
    
    return yy5mdd(s) and mod11(s)

#------------------------------------------------------------------------------
def mod11(item):

    s = re.sub(r'[ .\-/]', '', item)

    try   : i = int(s)
    except: return False
    
    # Ak je delitelne 11 vratim 1 inak 0
    if i%11 == 0: return True
    else        : return False

#------------------------------------------------------------------------------
def isTime(item):
    
    rx = re.findall("^\\d{2}[ .:-][A-Z]{3}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}[.]\\d{6} [AP]M|^\\d{4}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}|^\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}[ .:-]\\d{2}|^\\d{2}[.:-]\\d{2}[.:-]\\d{2}\\s*$|^\\d{2}:\\d{2}:\\d{2}$|^\\d{2}:\\d{2}$", item)
    
    if len(rx) > 0: return True

    return False

#------------------------------------------------------------------------------
def isDate(item):
    
    return isTime(item) or ddmmyyyy(item) or yyyymmdd(item)

#------------------------------------------------------------------------------
def ddmmyyyy(item):
    
    s = re.sub(r'[ .\-/]', '', item)
    
    # Ak neobsahuje aspon 6 cislic vratim 0
    if len(s) < 6: return False

    # Rozdelim string na zlozky
    try:
        dd = int(s[0:2])
        mm = int(s[2:4])
        
    except: return False
    
    # Test na datum
    try:
        if len(s) > 7: yy = int(s[4:8])
        else         : yy = int(s[4:6])
            
        d = date(yy, mm, dd)
        return True
    
    except: return False

#------------------------------------------------------------------------------
def yyyymmdd(item):
    
    s = re.sub(r'[ .\-/]', '', item)
    
    # Ak neobsahuje aspon 8 cislic vratim 0
    if len(s) < 8: return False

    # Test na datum
    try:
        yy = int(s[0:4])
        if (yy<1900) or (yy>2200): return False
        
        mm = int(s[4:6])
        dd = int(s[6:8])
        
        d = date(yy, mm, dd)
        return True
    
    except: return False

#------------------------------------------------------------------------------
def yy5mdd(s):
    
    # Ak neobsahuje aspon 6 cislic vratim 0
    if len(s) < 6: return False

    # Rozdelim string na zlozky
    try:
        yy = int(s[0:2])
        mm = int(s[2:4])
        dd = int(s[4:6])
        
    except: return False
    
    # Test na chlapcov
    try:
        d = date(yy, mm, dd)
        return True
    except: pass
    
    # Test na dievcata
    try:
        d = date(yy, mm-50, dd)
        return True
    except: pass
    
    # Neobsahuje datum
    return False

#------------------------------------------------------------------------------
def getMask(s):
    
    toRet = s

    if re.search(r'[A-ZĽĹŠČŤŽÝÁÍÉÚŇ]',    toRet): toRet = re.sub(r'[A-ZĽĹŠČŤŽÝÁÍÉÚŇ]',       'C', toRet)
    if re.search(r'[a-zľĺščťžýáäíéúňô]',  toRet): toRet = re.sub(r'[a-zľĺščťžýáäíéúňô]',     'c', toRet)
    if re.search(r'\d',                   toRet): toRet = re.sub(r'\d',                      'N', toRet)
    if re.search(r'\s',                   toRet): toRet = re.sub(r'\s+?',                    ' ', toRet)
        
    if re.search(r'[`~#$%^&\\\'\"/?§;:]', toRet): toRet = re.sub(r'[`~#$%^&\\\'\"/?§;:]+?',  '^', toRet)
        
    return toRet
        
#==============================================================================
# Persistency Tools
#------------------------------------------------------------------------------
def lines2str(lines, delim='\n'):
    
    toRet = ''

    for line in lines:
        toRet = toRet + line + delim
        
    return toRet
    
#------------------------------------------------------------------------------
def loadFile(journal, fileName, enc='utf-8'):
    
    toRet = []
    
    #--------------------------------------------------------------------------
    # Ak file existuje
    #--------------------------------------------------------------------------
    if os.path.exists(fileName): 
        
        try:
            with open(fileName, encoding=enc) as file:
                toRet = [line.replace('\n', '') for line in file]

            journal.M(f'SIQO.loadFile: From {fileName} was loaded {len(toRet)} lines')
        
        except Exception as err:
            journal.M('SIQO.loadFile: {} ERROR {}'.format(fileName, str(err)), True)
            
    #--------------------------------------------------------------------------
    # Ak json file NEexistuje
    #--------------------------------------------------------------------------
    else: journal.M(f'SIQO.loadFile: ERROR File {fileName} does not exist', True)
    
    #--------------------------------------------------------------------------
    return toRet

#------------------------------------------------------------------------------
def saveFile(journal, fileName, lines, enc='utf-8'):
    
    with open(fileName, 'w', encoding=enc) as file:

        for line in lines:
            file.write(line)

    journal.M(f'SIQO.saveFile: File {fileName} was saved')
        
#------------------------------------------------------------------------------
def loadJson(journal, fileName, enc='utf-8'):
    
    toret = None
    
    #--------------------------------------------------------------------------
    # Ak json file existuje
    #--------------------------------------------------------------------------
    if os.path.exists(fileName): 
        
        try:
            with open(fileName, encoding=enc) as file:
                toret = json.load(file)
                
            journal.M('SIQO.loadJson: From {} was loaded {} entries'.format(fileName, len(toret)))
                
        except Exception as err:
            journal.M('SIQO.loadJson: {} ERROR {}'.format(fileName, str(err)), True)
            
    #--------------------------------------------------------------------------
    # Ak json file NEexistuje
    #--------------------------------------------------------------------------
    else: journal.M('SIQO.loadJson: ERROR File {} does not exist'.format(fileName), True)
    
    #--------------------------------------------------------------------------
    return toret

#------------------------------------------------------------------------------
def dumpJson(journal, fileName, data, enc='utf-8'):
    
    try:
        file = open(fileName, "w", encoding=enc)
        json.dump(data, file, indent = 6)
        file.close()    

        journal.M('SIQO.dumpJson: {} saved'.format(fileName))

    except Exception as err:
        journal.M('SIQO.dumpJson: {} ERROR {}'.format(fileName, str(err)), True)
    
#------------------------------------------------------------------------------
def dumpCsv(journal, fileName, data):

    df = pd.DataFrame(data)
    df.to_csv(fileName, index=False)    
    
    journal.M('SIQO.dumpCsv: {} saved'.format(fileName))

#------------------------------------------------------------------------------
def picObj(journal, fileName, obj):
    
    dbfile = open(fileName, 'wb')
    pickle.dump(obj, dbfile)
    dbfile.close()
    
    journal.M('SIQO.picObj: {} saved'.format(fileName))

#------------------------------------------------------------------------------
def unPicObj(journal, fileName):
    
    dbfile = open(fileName, 'rb')
    obj = pickle.load(dbfile)
    dbfile.close()
    
    journal.M('SIQO.unPicObj: {} loaded'.format(fileName))
    return obj

#==============================================================================
# Dict % List Tools
#------------------------------------------------------------------------------
def dictString(dct):
    "Returns dictionary converted to a string"
    
    toRet = '{'
    
    for key, val in dct.items():
        
        if toRet != '{': toRet += ', '
            
        if   type(val)==dict: toRet += dictString(val)
        elif type(val)==list: toRet += listString(val)
        else                : toRet += f'{key}: {val}'
        
    toRet += '}'    
        
    return toRet
    
#------------------------------------------------------------------------------
def listString(lst):
    "Returns list converted to a string"
    
    toRet = '['
    
    for val in lst:
        
        if toRet != '[': toRet += ', '
            
        if   type(val)==dict: toRet += dictString(val)
        elif type(val)==list: toRet += listString(val)
        else                : toRet += f'{val}'
    
    toRet += ']'    
    
    return toRet
    
#------------------------------------------------------------------------------
def dictPrint(dct, indent=' ', depth=0):
    "Prints dictionaries"
    
    indent = ' ' * depth
    
    #--------------------------------------------------------------------------
    # List
    #--------------------------------------------------------------------------
    if type(dct) == list:
        
        cnt = 0
        for val in dct:
            
            if (type(val) in {dict, list}): dictPrint(val, indent, depth+1)
            else: print(f'{indent}[{cnt:10}]{val}')
            
            cnt += 1
            
    #--------------------------------------------------------------------------
    # Dict
    #--------------------------------------------------------------------------
    if type(dct) == dict:
        
        for key, val in dct.items():
            
            if (type(val) in {dict, list}): 
                
                print(f'{indent}[{key}]')
                dictPrint(val, indent, depth+1)
                
            else: print(f'{indent}{key:10}{val}')

#------------------------------------------------------------------------------
def dictLen(dct, left=99):
    "Returns len of immersed dictionaries"
    
    toRet = 0
    
    for val in dct.values():
        
        if (type(val) in {dict, list}) and (left>0): toRet += dictLen(val, left-1)
        else                                       : toRet += 1
            
    return toRet
    
#------------------------------------------------------------------------------
def dictSort(dct, sortKey=(1,), reverse=False):
    "Returns sorted dictionary"
    
    toRet = dct
    
    try:
        if len(sortKey) == 1: 
            toRet = dict( sorted(dct.items(), key=lambda item: item[sortKey[0]], reverse=reverse) )
    
        else:
            toRet = dict( sorted(dct.items(), key=lambda item: item[sortKey[0]][sortKey[1]], reverse=reverse) )
            
    finally:
        return toRet

#------------------------------------------------------------------------------
def listSort(lst, sortKey=None, reverse=False):
    "Returns sorted list of dictionaries"
    
    if sortKey is None: toRet = lst.sort(reverse=reverse)
    else              : toRet = sorted(lst, key=lambda val: val[sortKey], reverse=reverse)
    
    return toRet
    
#------------------------------------------------------------------------------
def listToDic(lst, keyLst=[]):
    "Returns list converted into dict with respective keys"

    toRet = {}
    i     = 0

    #--------------------------------------------------------------------------
    # Prejdem vsetky polozky v zozname
    #--------------------------------------------------------------------------
    for item in lst:
        
        # Vytvorim kluc
        keyStr = ''
        for key in keyLst: keyStr += str(item[key])
        
        # Vlozim item do dict pod klucom
        if keyStr not in toRet.keys(): toRet[keyStr] = []
            
        toRet[keyStr].append(item)
        
        i += 1
            
    #--------------------------------------------------------------------------
    return (toRet, i)

#------------------------------------------------------------------------------
def listDicComp(refLst, tstLst, keyLst):
    "Returns differences between lists of Dictionaries"

    toRet = {'missingInTst':{}, 'extraInTst':{}, 'differ':{}}
 
    (refDic, refI) = listToDic(refLst, keyLst)
    (tstDic, tstI) = listToDic(tstLst, keyLst)

    #--------------------------------------------------------------------------
    # Prejdem vsetky polozky v Ref
    #--------------------------------------------------------------------------
    for refKey, ref in refDic.items():
        
        # Skontrolujem, ci sa nachadza aj v tst
        if refKey in tstDic.keys():
            
            pass
            
 #           diff = dicDiffer(ref, tstDic[refKey])
            
            # Skontrolujem, ci su rovnake hodnoty
 #           if len(diff) > 0: 
                
 #               if refKey not in toRet['differ'].keys(): toRet['differ'][refKey] = []
 #               toRet['differ'][refKey].append(diff)
            
        else: 
            
#            if refKey not in toRet['missingInTst'].keys(): toRet['missingInTst'][refKey] = []
#            toRet['missingInTst'][refKey].append(ref)            
            toRet['missingInTst'][refKey] = ref            
            
    #--------------------------------------------------------------------------
    # Prejdem vsetky polozky v Tst
    #--------------------------------------------------------------------------
    for tstKey, tst in tstDic.items():
        
        # Skontrolujem, ci sa nachadza aj v ref
        if tstKey not in refDic.keys(): 
            
#            if tstKey not in toRet['extraInTst'].keys(): toRet['extraInTst'][tstKey] = []
#            toRet['extraInTst'][tstKey].append(tst)            
            toRet['extraInTst'][tstKey] = tst            
     
    #--------------------------------------------------------------------------
    return toRet
    
#------------------------------------------------------------------------------
def dicDiffer(ref, tst):
    "Returns differences between two simple Dictionaries"
    
    toRet = {}
    
    #--------------------------------------------------------------------------
    # Prejdem vsetky polozky v Ref
    #--------------------------------------------------------------------------
    for refKey in ref.keys():
        
        # Skontrolujem, ci sa nachadza aj v tst
        if refKey in tst.keys():
            
            # Skontrolujem, ci su rovnake hodnoty
            if ref[refKey] != tst[refKey]: toRet[refKey] = {'key':refKey, 'ref':ref[refKey], 'tst':tst[refKey]}
            
        else: toRet[refKey] = {'key':refKey, 'ref':ref[refKey], 'tst':None}
        
    #--------------------------------------------------------------------------
    # Prejdem vsetky polozky v Tst
    #--------------------------------------------------------------------------
    for tstKey in tst.keys():
        
        # Skontrolujem, ci sa nachadza aj v ref
        if tstKey not in ref.keys(): toRet[tstKey] = {'key':refKey, 'ref':None, 'tst':tst[tstKey]}
        
    #--------------------------------------------------------------------------
    return toRet
    
#==============================================================================
# Base64 Tools
#------------------------------------------------------------------------------
def b64enc(s):

    return base64.b64encode(s.encode("ascii")).decode('ascii')
    
#------------------------------------------------------------------------------
def b64dec(s):
    
    return base64.b64decode(s.encode('ascii')).decode('ascii')
    
#------------------------------------------------------------------------------
def getPasw(journal, con, user):
    
    journal.I(f"SIQO.getPasw: '{con}', '{user}'")
    
    envKey   = f'PWD_{con.upper()}_{user.upper()}'
    b64_pasw = os.environ.get(envKey, None)
    
    if b64_pasw is None:
        journal.M(f"SIQO.getPasw: WARNING - Password for '{envKey}' does not exist", True)
        journal.O()
        return None
    
    journal.O()
    return b64dec(b64_pasw)

#==============================================================================
#   Inicializacia kniznice
#------------------------------------------------------------------------------

print('SIQO general library ver 1.13')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------