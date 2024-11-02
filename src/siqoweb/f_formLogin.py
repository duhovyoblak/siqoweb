#==============================================================================
#  SIQO Homepage: Form Login
#------------------------------------------------------------------------------
import os

from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from f_form             import PgForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.01'
_CWD      = os.getcwd()

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# FormLogin
#------------------------------------------------------------------------------
class FormLogin(PgForm):
    
    username = StringField  ('Username', validators=[DataRequired()] )
    password = PasswordField('Password', validators=[DataRequired()] )
    remember = BooleanField ('Remember Me')
    
    login   = SubmitField('Sign In')
    asGuest = SubmitField('Continue as Guest User')
    logout  = SubmitField('Sign Out')

#==============================================================================
print(f"forms {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
