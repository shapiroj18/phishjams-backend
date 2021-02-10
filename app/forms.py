from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UnsubscribeEmail(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
