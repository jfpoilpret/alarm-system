from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length

from app.models import Account

class AbstractUserForm(Form):
    username = StringField('User Name', validators=[InputRequired(), Length(3, 64)])
    fullname = StringField('Full Name', validators=[InputRequired(), Length(4, 128)])
    role = SelectField('Role', coerce=int, choices = 
        [(Account.ROLE_ALARM_VIEWER, 'Alarm Viewer'),
         (Account.ROLE_ALARM_SETTER, 'Alarm Setter'),
         (Account.ROLE_CONFIGURATOR, 'Configurator'),
         (Account.ROLE_ADMINISTRATOR, 'Administrator')])

# Form to edit an existing user
class EditUserForm(AbstractUserForm):
    submit = SubmitField('Save User')

# Form to create a new user
#TODO missing validators on password
class NewUserForm(AbstractUserForm):
    password = PasswordField('Password')
    submit = SubmitField('Create User')
