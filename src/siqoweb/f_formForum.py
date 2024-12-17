#==============================================================================
#  SIQO Homepage: Form for object Forum
#------------------------------------------------------------------------------
import os

from wtforms            import StringField, TextAreaField, BooleanField, SubmitField
from wtforms            import validators

from f_form             import FormStruct

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.02'
_CWD      = os.getcwd()

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# FormForum
#------------------------------------------------------------------------------
class FormForum(FormStruct):
    
    parent_id    = StringField  ('Parent ID', validators=[validators.DataRequired()])
    user_id      = StringField  ('User ID',   validators=[validators.DataRequired()]) 
    title        = StringField  ('Title',     validators=[validators.DataRequired()])
    narrator     = StringField  ('Narrator',  validators=[validators.DataRequired()])
    item         = TextAreaField('Item',      validators=[validators.DataRequired()])
    
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
