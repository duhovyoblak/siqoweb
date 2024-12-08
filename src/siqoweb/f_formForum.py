#==============================================================================
#  SIQO Homepage: Form for object Forum
#------------------------------------------------------------------------------
import os

from wtforms            import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from f_form             import FormStruct

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
class FormForum(FormStruct):
    
    narrator     = StringField  ('Narrator')
    text         = TextAreaField('Text'    )
    
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
print(f"formForum {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
