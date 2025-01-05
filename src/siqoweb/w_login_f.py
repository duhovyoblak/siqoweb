#==============================================================================
#  SIQO Homepage: Form Login
#------------------------------------------------------------------------------
from wtforms            import StringField, PasswordField, BooleanField, SubmitField
from wtforms            import validators

from w__window_f        import WindowForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# FormLogin
#------------------------------------------------------------------------------
class LoginForm(WindowForm):
    
#    WindowForm.formType.
    
    username   = StringField  ('Username', validators=[validators.Optional()] )
    password   = PasswordField('Password', validators=[validators.Optional()] )
    remember   = BooleanField ('Remember Me')
    
    btnLogin   = SubmitField('Sign In')
    btnGuest   = SubmitField('Continue as Guest User')
    btnLogout  = SubmitField('Sign Out')

#==============================================================================
print(f"w_login_f {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
