#==============================================================================
#  SIQO Homepage: Formulars
#------------------------------------------------------------------------------
import os

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = 1.00
_IS_TEST  = True if os.environ['wsiqo-test-mode']=='1' else False

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# 
#------------------------------------------------------------------------------
class FormLogin(FlaskForm):
    
    username    = StringField  ('Username', validators=[DataRequired()] )
    password    = PasswordField('Password', validators=[DataRequired()] )
    remember_me = BooleanField ('Remember Me')
    
    submit = SubmitField('Sign In')
    



#==============================================================================
print(f"forms {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
