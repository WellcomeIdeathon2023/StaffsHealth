from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField('Username:', validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
    contact_method_choices = {"WhatsApp": "whatsapp", "Instagram": "instagram", "Facebook": "facebook",
                              "Phone": "phone"}
    contact_method = SelectField("Method of contact:", choices = contact_method_choices)

    phone_number = StringField('Phone number:', validators=[DataRequired()])
    submit = SubmitField('Submit')
