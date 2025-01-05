#==============================================================================
#  SIQO Homepage: Configuration
#------------------------------------------------------------------------------
import os
import siqoweb

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Config class
#------------------------------------------------------------------------------
class Config:
    
    packPath    = os.path.dirname(siqoweb.__file__)

    dtbsPath    = f"{packPath}/database/"
    dtbsName    = "pagman"
    
    tabParam    = "PM_PARAM"
    
    tabUser     = "PM_USER"
    tabObj      = "PM_OBJECT"
    tabObjRes   = "PM_OBJ_RESOURCE"
    tabObjRole  = "PM_OBJ_USER_ROLE"
    tabObjCache = "PM_OBJ_CACHE"

    #--------------------------------------------------------------------------
    # DMS
    #--------------------------------------------------------------------------
    tabDms      = "PM_DMS"

    dmsFolder   = "dms"
    dmsPrefix   = 'SF'
    dmsFnLen    = 7

    #--------------------------------------------------------------------------
    # Forum
    #--------------------------------------------------------------------------
    tabForum    = "PM_FORUM"

    if 'wsiqo-secret-key' in os.environ: SECRET_KEY = os.environ.get('wsiqo-secret-key')
    else                               : SECRET_KEY = "ekjwn47wtyqgpUHP43UGH3"

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    


    print(Config.SECRET_KEY)
    
#==============================================================================
print(f"config {_VER}")

print('Config packPath :', Config.packPath  )
print('Config dtbsPath :', Config.dtbsPath  )
print('Config dtbsName :', Config.dtbsName  )
print('Config tabUser  :', Config.tabUser   )
print('Config dmsFolder:', Config.dmsFolder )

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
