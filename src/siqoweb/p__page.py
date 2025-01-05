#==============================================================================
#  SIQO web library: Function for SIQO Flask application
#------------------------------------------------------------------------------
from   flask                    import url_for, get_flashed_messages, flash, make_response
from   flask                    import request, session, abort, redirect
from   flask_login              import login_user, logout_user, current_user

from   markupsafe               import escape
from   wtforms.validators       import ValidationError

from   siqoweb.config           import Config
from   siqoweb.app_dms          import DMS
from   siqoweb.p__structure     import Structure

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Page
#------------------------------------------------------------------------------
class Page(Structure):
    
    #==========================================================================
    # Constructor & Tools
    #--------------------------------------------------------------------------
    def __init__(self, journal, title, classId, height, idx=0):
        "Call constructor of Page and initialise it"
        
        journal.I(f"Page({classId}).init:")
        
        #----------------------------------------------------------------------
        # Identifikacia usera
        #----------------------------------------------------------------------
        user = current_user
        
        if user is not None and str(user)[:5]=='User>': 
            
            userId   = user.user_id
            userName = user.userName()
            lang     = user.lang_id
            
        else: 
            userId   = 'Anonymous'
            userName = 'Guest User'
            lang     = 'SK'

        #----------------------------------------------------------------------
        # Konstruktor DMS/Database
        #----------------------------------------------------------------------
        dms  = DMS (journal, Config.dtbsName, Config.dtbsPath)

        #----------------------------------------------------------------------
        # Konstruktor Page Structure
        #----------------------------------------------------------------------
        super().__init__(journal, dms, title, userId, userName, lang, classId, height, idx)
        
        self.name     = f"Page({self.name})"

        #----------------------------------------------------------------------
        # Aktualny user a jazyk
        #----------------------------------------------------------------------
        journal.M(f"{self.name}).init: user = '{self.userName}'")
        journal.M(f"{self.name}).init: lang = '{self.lang}'"    )
        journal.M(f"{self.name}).init: idx  = '{self.idx}'"     )

        self.journal.O()
       
    #==========================================================================
    # Response generators
    #--------------------------------------------------------------------------
    def resp(self):
     
        self.journal.I(f"{self.name}.resp:")
        
        #----------------------------------------------------------------------
        # Vypisem si request data
        #----------------------------------------------------------------------
#        self.journal.M(f"{self.name}.resp: user_agent       {request.user_agent}")
        self.journal.M(f"{self.name}.resp: remote_addr      {request.remote_addr}" )
        self.journal.M(f"{self.name}.resp: is_secure        {request.is_secure}"   )
#        self.journal.M(f"{self.name}.resp: form             {request.form}")
        self.journal.M(f"{self.name}.resp: data             {request.data}"        )
        self.journal.M(f"{self.name}.resp: args             {request.args}"        )
        self.journal.M(f"{self.name}.resp: access_route     {request.access_route}")

        self.journal.M(f"{self.name}.resp: headers.Referer  {request.headers.get('Referer')}")
#        self.journal.M(f"{self.name}.resp: headers.Cookie   {request.headers.get('Cookie' )}")



        #----------------------------------------------------------------------
        # Skontrolujem stav stranky, vyskocim ak nie je pripravena
        #----------------------------------------------------------------------
        if not self.loaded:
            self.journal.O()
            abort(500)
        
        #----------------------------------------------------------------------
        # POST Method: Vyhodnotim formulare
        #----------------------------------------------------------------------
        if request.method == 'POST':
            
            try: resp = self.respPost()
            except ValidationError as err: print(str(err))
            
            #------------------------------------------------------------------
            # Ak je POST response validna
            #------------------------------------------------------------------
            if resp is not None:
                self.journal.O()
                return resp

        #----------------------------------------------------------------------
        # Default response:
        #----------------------------------------------------------------------
        resp = self.respGet()
        self.journal.O()
        return resp

    #--------------------------------------------------------------------------
    def respPost(self):
     
        self.journal.I(f"{self.name}.respPost: Default None POST response")
        resp = None
        
        self.journal.M(f"{self.name}.respPost: idx   > {self.idx}",    True)
        #self.journal.M(f"{self.name}.respPost: POST  > {self.POST}",   True)

        #----------------------------------------------------------------------
        # Prejdem vsetky windows
        #----------------------------------------------------------------------
        for winId, winObj in self.windows().items():
            
            #------------------------------------------------------------------
            # Kontrola prislusnosti response
            #------------------------------------------------------------------
            #if winObj.
            resp = winObj.respPost()
        
        #----------------------------------------------------------------------
        self.journal.O()
        return resp

    #--------------------------------------------------------------------------
    def respGet(self):
     
        self.journal.I(f"{self.name}.respGet: Default GET response ")
        
        #----------------------------------------------------------------------
        # Vygenerujem html response
        #----------------------------------------------------------------------
        resp = make_response(self.html(), 200)
        
        # V pripade potreby vies doplnit headers o custom data
        # resp.headers['X-Something'] = 'A value'
        
        self.journal.O()
        return resp

#==============================================================================
# Test cases
#------------------------------------------------------------------------------
if __name__ == '__main__':
    
    from   siqolib.journal              import SiqoJournal
    journal = SiqoJournal('test-base', debug=5)
    
    page = Page(journal, 'Homepage', 'PagManLogin', 700)
#    page = Page(journal, 'Homepage', 'PagManHomepage', 700)
    print(page)
    

#==============================================================================
print(f"Page {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
