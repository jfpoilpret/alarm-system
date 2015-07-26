from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Regexp
from wtforms.fields.core import FloatField
from wtforms.fields.simple import HiddenField
from flask.ext.wtf.file import FileField, FileAllowed
from app.common import HiddenInteger

# Form to create a new configuration (general information only)
class AbstractConfigForm(Form):
    id = HiddenInteger(default = 0)
    name = StringField('Name', validators = [InputRequired(), Length(1, 64)])
    lockcode = StringField('Lock code', validators = [InputRequired(), Regexp('[0-9]{6}')])
    map_area_file = FileField("Monitored Zone Map", 
        validators = [FileAllowed(['svg'], 'Map must be a vectorial image (SVG) only!')])
    map_area_filename = StringField('Map Source File', validators = [Length(0, 256)])

class NewConfigForm(AbstractConfigForm):
    submit = SubmitField('Create Configuration')

# Form to edit an existing configuration (general information only)
class EditConfigForm(AbstractConfigForm):
    submit = SubmitField('Save Configuration')

# Special form to setup devices location (and only that): JavaScript based
class DevicesLocationForm(Form):
    id = HiddenInteger(default = 0)
    devices_locations = HiddenField('JSONLocations')
    submit = SubmitField('Save Modules Location')

class AbstractDeviceForm(Form):
    id = HiddenInteger(default = 0)
    config_id = HiddenInteger()
    name = StringField('Name', validators = [InputRequired(), Length(1, 64)])
    kind = HiddenInteger()
    voltage_threshold = FloatField('Voltage Threshold', validators = [InputRequired()])
    device_id = SelectField('Module ID', coerce = int)

class NewDeviceForm(AbstractDeviceForm):
    submit = SubmitField('Add')

class EditDeviceForm(AbstractDeviceForm):
    submit = SubmitField('Save')
