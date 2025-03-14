#==============================================================================
#  SIQO Homepage: Basic root Formulars
#------------------------------------------------------------------------------
from flask_wtf                  import FlaskForm
from wtforms                    import HiddenField, StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms                    import validators

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# Form
#------------------------------------------------------------------------------
class WindowForm(FlaskForm):
    
    formType = HiddenField('WindowForm',    validators=[validators.Optional()])

#==============================================================================
print(f"w_window_f {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
