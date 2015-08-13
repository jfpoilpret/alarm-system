from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length

from app.models import Account
from app.common import HiddenInteger

ROLES = [
    (Account.ROLE_ADMINISTRATOR, 'Administrator'),
    (Account.ROLE_CONFIGURATOR, 'Configurator'),
    (Account.ROLE_ALARM_SETTER, 'Alarm Setter'),
    (Account.ROLE_ALARM_VIEWER, 'Alarm Viewer'),
]

class AbstractUserForm(Form):
    id = HiddenInteger(default = 0)
    username = StringField('User Name', validators=[InputRequired(), Length(3, 64)])
    fullname = StringField('Full Name', validators=[InputRequired(), Length(4, 128)])
    role = SelectField('Role', choices = [(label, label) for (_, label) in ROLES])

# Form to edit an existing user
class EditUserForm(AbstractUserForm):
    submit = SubmitField('Save User')

# Form to create a new user
class NewUserForm(AbstractUserForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(3, 64)])
    submit = SubmitField('Create User')
