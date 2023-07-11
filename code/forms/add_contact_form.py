from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime


class AddContactForm(FlaskForm):
    date = DateField(validators=[DataRequired()],
                     default=datetime.today,
                     render_kw={"placeholder": "Message Date:"})
    time = TimeField(validators=[DataRequired()],
                     render_kw={"placeholder": "Message Time:"})
    message = StringField("Message:", validators=[DataRequired()],
                          render_kw={"placeholder": "What message is required"})
    submit_AddContactForm = SubmitField('Submit')
