#==============================================================================
#  SIQO Homepage: Form for object Forum
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
# FormForum
#------------------------------------------------------------------------------
class FormForum(PgForm):
    
    username = StringField  ('Username', validators=[DataRequired()] )
    password = PasswordField('Password', validators=[DataRequired()] )
    remember = BooleanField ('Remember Me')
    
    sfUp         = SubmitField('Up')
    sfEdit       = SubmitField('Edit')
    sfAddChapter = SubmitField('Add Chapter')
    afAddChild   = SubmitField('Add Child')
    sfApply      = SubmitField('Apply')
    sfCancel     = SubmitField('Cancel')
    sfPublish    = SubmitField('Publish')
    sfDelete     = SubmitField('Delete')
    sfMove       = SubmitField('Move To')
    

#==============================================================================
print(f"forms {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
