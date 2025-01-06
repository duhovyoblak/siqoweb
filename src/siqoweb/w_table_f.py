#==============================================================================
#  SIQO Homepage: Form for object Table
#------------------------------------------------------------------------------
from wtforms                    import HiddenField, StringField, TextAreaField, IntegerField, SubmitField
from wtforms                    import FieldList, FormField
from wtforms                    import validators

from siqoweb.w__window_f        import WindowForm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_VER      = '1.01'

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# FormTable
#------------------------------------------------------------------------------
from flask_wtf import FlaskForm
from wtforms.widgets import HTMLString, html_params

#==============================================================================
# Custom field TableField with widget
#------------------------------------------------------------------------------
class TableWidget(object):

    #--------------------------------------------------------------------------
    def __call__(self, field, **kwargs):
        "Returns html code for <field> of type TableField"
        
        #----------------------------------------------------------------------
        # Ensures there is 'id' if kwargs dict keys
        #----------------------------------------------------------------------
        kwargs.setdefault('id', field.id)
        
        #----------------------------------------------------------------------
        # Starts html output
        #----------------------------------------------------------------------
        html = ['<table %s>' % html_params(**kwargs)]
        
        
        for subfield in field:
            html.append('<tr>')
            for col in subfield:
                html.append('<td>%s</td>' % col())
            html.append('</tr>')
            
        #----------------------------------------------------------------------
        # Ends html output
        #----------------------------------------------------------------------
        html.append('</table>')
        
        return HTMLString(''.join(html))

#------------------------------------------------------------------------------
class TableField(FieldList):
    "Defines TableField as FieldList with widget=TableWidget"
    
    widget = TableWidget()

#==============================================================================
# Custom field RowField
#------------------------------------------------------------------------------
class RowForm(FlaskForm):
    
    col1 = StringField('Column 1')
    col2 = StringField('Column 2')

#==============================================================================
# TableForm
#------------------------------------------------------------------------------
class TableForm(WindowForm):
    
    rows = TableField(FormField(RowForm), min_entries=3)


#==============================================================================
print(f"w_forum_f {_VER}")

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
