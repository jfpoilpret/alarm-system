from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Regexp
from wtforms.fields.core import FloatField
from wtforms.fields.simple import HiddenField
from flask.ext.wtf.file import FileField, FileAllowed

# Form to create a new configuration (general information only)
#TODO show extra (readonly) field with latest upload filename
class AbstractConfigForm(Form):
    name = StringField('Name', validators = [InputRequired(), Length(1, 64)])
    lockcode = StringField('Lock code', validators = [InputRequired(), Regexp('[0-9]{6}')])
    map_area_file = FileField("Monitored Zone Map", 
        validators = [FileAllowed(['svg'], 'Map must be a vectorial image (SVG) only!')])

class NewConfigForm(AbstractConfigForm):
    submit = SubmitField('Create Configuration')

# Form to edit an existing configuration (general information only)
class EditConfigForm(AbstractConfigForm):
    submit = SubmitField('Save Configuration')

# Special form to setup devices location (and only that): JavaScript based
class DevicesLocationForm(Form):
    devices_locations = HiddenField('JSONLocations')
    submit = SubmitField('Save Modules Location')

class AbstractDeviceForm(Form):
    name = StringField('Name', validators = [InputRequired(), Length(1, 64)])
    kind = HiddenField('Kind')
    voltage_threshold = FloatField('Voltage Threshold', validators = [InputRequired()])
    device_id = SelectField('Module ID', coerce = int)

class NewDeviceForm(AbstractDeviceForm):
    submit = SubmitField('Add Module')

class EditDeviceForm(AbstractDeviceForm):
    submit = SubmitField('Save Module')
