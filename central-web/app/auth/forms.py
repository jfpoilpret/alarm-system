from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length

class SigninForm(Form):
    username = StringField('User Name', id = 'signin_username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', id = 'signin_password', validators=[Required()])
    submit = SubmitField('Sign In', id = 'signin_submit')

