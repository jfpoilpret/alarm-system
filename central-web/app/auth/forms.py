from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class SigninForm(Form):
    username = StringField('User Name', validators=[InputRequired(), Length(1, 64)])
    password = PasswordField('Password')
    submit = SubmitField('Sign In')

# Form to edit user profile
class ProfileForm(Form):
    username = StringField('User Name', validators=[InputRequired(), Length(3, 64)])
    fullname = StringField('Full Name', validators=[InputRequired(), Length(4, 128)])
    submit = SubmitField('Save Profile')

class PasswordForm(Form):
    password = PasswordField('New Password', validators=[InputRequired(), Length(3, 64)])
    repeat_password = PasswordField('Repeat Password', validators=[InputRequired(), Length(3, 64)])
    submit = SubmitField('Save Password')
