#==============================================================================
#  SIQO Homepage: Form Login
#------------------------------------------------------------------------------
import os

from wtforms            import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from p__page_f          import PageForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'
_CWD      = os.getcwd()

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# FormLogin
#------------------------------------------------------------------------------
class LoginForm(PageForm):
    
    username   = StringField  ('Username', validators=[DataRequired()] )
    password   = PasswordField('Password', validators=[DataRequired()] )
    remember   = BooleanField ('Remember Me')
    
    btnLogin   = SubmitField('Sign In')
    btnGuest   = SubmitField('Continue as Guest User')
    btnLogout  = SubmitField('Sign Out')

#==============================================================================
print(f"forms {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
