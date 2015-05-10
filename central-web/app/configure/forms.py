from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, Regexp
from wtforms.fields.core import FloatField
from wtforms.fields.simple import HiddenField
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed

# Form to create a new configuration (general information only)
class ConfigForm(Form):
    name = StringField('Name', validators = [DataRequired(), Length(1, 64)])
    lockcode = StringField('Lock code', validators = [DataRequired(), Regexp('[0-9]{6}')])
    map_area = FileField("Monitored Zone Map", 
        validators = [FileAllowed(['svg'], 'Map must be a vectorial image (SVG) only!')])
    submit = SubmitField('Create Configuration')

# Form to edit an existing configuration (general information only)
class EditConfigForm(ConfigForm):
    submit = SubmitField('Save Configuration')

#TODO remove in the end
class ConfigMapForm(Form):
    map_area = FileField("Monitored Zone Map", 
        validators = [FileRequired(), FileAllowed(['svg'], 'Map must be a vectorial image (SVG) only!')])
    submit = SubmitField('Save Map Image')

#TODO special form to setup devices location (and only that): JavaScript based
class DevicesLocationForm(Form):
    devices_locations = HiddenField('JSONLocations')
    submit = SubmitField('Save Modules Location')

class DeviceForm(Form):
    name = StringField('Name', validators = [DataRequired(), Length(1, 64)])
    kind = HiddenField('Kind')
    voltage_threshold = FloatField('Voltage Threshold')
    device_id = SelectField('Module ID', coerce = int)
    submit = SubmitField('Add Module')

class EditDeviceForm(DeviceForm):
    submit = SubmitField('Save Module')
