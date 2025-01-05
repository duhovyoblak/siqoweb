#==============================================================================
#  SIQO Homepage: Form for object Forum
#------------------------------------------------------------------------------
from wtforms                    import HiddenField, StringField, TextAreaField, IntegerField, SubmitField
from wtforms                    import validators

from siqoweb.w__window_f        import WindowForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.04'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# FormForum
#------------------------------------------------------------------------------
class ForumForm(WindowForm):
    
    itemId       = StringField  ('Item ID',             validators=[validators.ReadOnly() ])

    parentId     = StringField  ('Parent ID',           validators=[validators.DataRequired()]) 
    userId       = StringField  ('User ID',             validators=[validators.ReadOnly()]) 
    title        = StringField  ('Title',               validators=[validators.DataRequired()])
    narrator     = StringField  ('Narrator',            validators=[validators.DataRequired()])
    
    text         = TextAreaField('Text',                validators=[validators.DataRequired()])
    
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
