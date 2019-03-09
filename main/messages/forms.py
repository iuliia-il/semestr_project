from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class AddMessageForm(FlaskForm):
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField('Message')
