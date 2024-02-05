#==============================================================================
#  SIQO Homepage: Configuration
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
# Config class
#------------------------------------------------------------------------------
class Config:
    
    cwd      = os.getcwd()
    
    dtbsPath = f"{cwd}/database/"
    dtbsName = "pagman"
    
    tabUser     = "SUSER"
    tabObj      = "SOBJECT"
    tabObjRes   = "SOBJ_RESOURCE"
    tabObjRole  = "SOBJ_USER_ROLE"
    tabObjCache = "SOBJ_CACHE"

    if 'wsiqo-secret-key' in os.environ: SECRET_KEY = os.environ.get('wsiqo-secret-key')
    else                               : SECRET_KEY = "ekjwn47wtyqgpUHP43UGH3"

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    print(Config.cwd       )
    print(Config.dtbsPath  )
    print(Config.dtbsName  )
    print(Config.tabUser  )


    print(Config.SECRET_KEY)
    
#==============================================================================
print(f"config {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
