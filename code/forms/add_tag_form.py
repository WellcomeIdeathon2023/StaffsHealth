from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AddTagForm(FlaskForm):
    tag = StringField('Tag:', validators=[DataRequired()], render_kw={"placeholder": "Enter new tag"})
    submit_AddTagForm = SubmitField('Submit')
