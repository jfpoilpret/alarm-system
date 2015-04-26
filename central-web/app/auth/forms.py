from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length

class SigninForm(Form):
    username = StringField('User Name', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password')
    submit = SubmitField('Sign In')

