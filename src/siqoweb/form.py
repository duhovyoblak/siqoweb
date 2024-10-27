#==============================================================================
#  SIQO Homepage: Basic root Formulars
#------------------------------------------------------------------------------
import os

from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.01'
_CWD      = os.getcwd()

if 'siqo-test' in os.environ: _IS_TEST = True if os.environ['siqo-test']=='1' else False 
else                        : _IS_TEST = False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Form
#------------------------------------------------------------------------------
class FormLogin(FlaskForm):
    
    UserActType  = SubmitField('Sign In')
    UserObj  = SubmitField('Continue as Guest User')
    UserAct = SubmitField('Sign Out')

#==============================================================================
# FormLogin
#------------------------------------------------------------------------------
class FormLogin(FlaskForm):
    
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
