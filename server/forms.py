from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

#Login form class for Email/Password to sign in  
class LoginForm(Form):
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
