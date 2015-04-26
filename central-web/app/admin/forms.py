from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import Length, DataRequired

from app.models import Account

# Form to edit an existing user
class EditUserForm(Form):
    username = StringField('User Name', validators=[DataRequired(), Length(3, 64)])
    fullname = StringField('Full Name', validators=[DataRequired(), Length(4, 128)])
    role = SelectField('Role', coerce=int, choices = 
        [(Account.ROLE_ALARM_VIEWER, 'Alarm Viewer'),
         (Account.ROLE_ALARM_SETTER, 'Alarm Setter'),
         (Account.ROLE_CONFIGURATOR, 'Configurator'),
         (Account.ROLE_ADMINISTRATOR, 'Administrator')])
    submit = SubmitField('Save User')

# Form to create a new user
class NewUserForm(EditUserForm):
    password = PasswordField('Password')
    submit = SubmitField('Create User')
