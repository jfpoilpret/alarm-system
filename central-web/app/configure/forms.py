from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, Regexp
from wtforms.fields.core import FloatField
from wtforms.fields.simple import HiddenField

#TODO remove from_model/to_model as long as fields are named same as models properties
# then use populate_obj(obj) and __init__(obj=xxx) to/from model
#TODO use same names for fields and id? => can we just remove id attribute?
# Form to create a new configuration (general information only)
class ConfigForm(Form):
    name = StringField('Name', id = 'config_name', validators=[DataRequired(), Length(1, 64)])
    #FIXME limite input to digits only!
    lockcode = StringField('Lock code', id = 'config_lockcode', validators=[DataRequired(), Regexp('[0-9]{6}')])
    submit = SubmitField('Create Configuration', id = 'config_submit')

    def from_model(self, config):
        self.name.data = config.name
        self.lockcode.data = config.lockcode

    def to_model(self, config):
        config.name = self.name.data
        config.lockcode = self.lockcode.data

# Form to edit an existing configuration (general information only)
class EditConfigForm(ConfigForm):
    submit = SubmitField('Save Configuration', id = 'config_submit')

class DeviceForm(Form):
    name = StringField('Name', id = 'name', validators=[DataRequired(), Length(1, 64)])
    kind = HiddenField('Kind', id = 'kind')
    voltage_threshold = FloatField('Voltage Threshold', id = 'voltage_threshold')
    device_id = SelectField('Module ID', id = 'device_id', coerce=int)
    submit = SubmitField('Add Module', id = 'device_save')

class EditDeviceForm(DeviceForm):
    submit = SubmitField('Save Module', id = 'device_save')
