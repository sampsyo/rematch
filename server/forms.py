from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, StringField
from wtforms.validators import DataRequired, EqualTo


# Login form class for Email/Password to sign in
class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    net_id = StringField('Net ID', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    is_student = BooleanField('I am a student')
