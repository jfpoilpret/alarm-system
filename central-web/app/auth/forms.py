from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, DataRequired

class SigninForm(Form):
    username = StringField('User Name', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password')
    submit = SubmitField('Sign In')

# Form to edit user profile
class ProfileForm(Form):
    username = StringField('User Name', validators=[DataRequired(), Length(3, 64)])
    fullname = StringField('Full Name', validators=[DataRequired(), Length(4, 128)])
    submit = SubmitField('Save Profile')

class PasswordForm(Form):
    password = PasswordField('New Password', validators=[DataRequired(), Length(3, 64)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), Length(3, 64)])
    submit = SubmitField('Save Password')
