#==============================================================================
#  SIQO Homepage: Form for object Forum
#------------------------------------------------------------------------------
import os

from wtforms            import HiddenField, StringField, TextAreaField, IntegerField, SubmitField
from wtforms            import validators

from w__window_f        import WindowForm

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
class ForumForm(WindowForm):
    
    itemId       = StringField  ('Item ID',             validators=[validators.ReadOnly() ])

    title        = StringField  ('Title',               validators=[validators.DataRequired()])
    user_id      = StringField  ('User ID',             validators=[validators.DataRequired()]) 
    narrator     = StringField  ('Narrator',            validators=[validators.DataRequired()])
    
    item         = TextAreaField('Text',                validators=[validators.DataRequired()])
    
    sfUp         = SubmitField  ('Up'                       )
    sfAddChapter = SubmitField  ('Add new Chapter'          )
    afAddChild   = SubmitField  ('Add Child to this Chapter')
    sfCancel     = SubmitField  ('Cancel any changes'       )
    sfApply      = SubmitField  ('Apply changes'            )
    sfPublish    = SubmitField  ('Publish this Chapter'     )
    sfDelete     = SubmitField  ('Delete this Chapter'      )
    sfMove       = SubmitField  ('Move this Chapter'        )
    

#==============================================================================
print(f"w_forum_f {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------