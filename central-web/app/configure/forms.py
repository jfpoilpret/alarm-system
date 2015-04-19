from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, Regexp
from wtforms.fields.core import IntegerField, FloatField
from wtforms.fields.simple import HiddenField
from flask_wtf.form import _Auto

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
    name = StringField('Name', id = 'device_name', validators=[DataRequired(), Length(1, 64)])
    kind = SelectField('Kind', id = 'device_kind', choices = [(1, 'Keypad'), (2, 'Motion'), (3, 'Camera')])
    voltage_threshold = FloatField('Voltage Threshold', id = 'device_voltage')
    device_id = IntegerField('Device ID', id = 'device_id', validators=DataRequired())
    submit = SubmitField('Add Device', id = 'device_create')

    def from_model(self, device):
        self.name.data = device.name
        self.kind.data = device.kind
        self.voltage_threshold.data = device.voltage_threshold
        self.device_id.data = device.device_id

    def to_model(self, device):
        device.name = self.name.data
        device.kind = self.kind.data
        device.voltage_threshold = self.voltage_threshold.data
        device.device_id = self.device_id.data

class AbstractDeviceForm(Form):
    wizard_step = HiddenField(id = 'wizard_step')
    config_id = HiddenField(id = 'config_id')
    id = HiddenField(id = 'id')
    name = HiddenField(id = 'device_name')
    kind = HiddenField(id = 'device_kind')
    voltage_threshold = HiddenField(id = 'device_voltage')
    device_id = HiddenField(id = 'device_id')
    
    cancel = SubmitField('Cancel', id = 'cancel')
    previous = SubmitField('<<', id = 'previous')
    next = SubmitField('>>', id = 'next')
    save = SubmitField('Save', id = 'save')
    save_and_new = SubmitField('Save & Continue', id = 'save_and_new')

    def get_step(self):
        return self.wizard_step.data

    def set_step(self, step):
        self.wizard_step.data = step

    def from_model(self, device):
        self.config_id.data = device.config_id
        self.id.data = device.id
        self.name.data = device.name
        self.kind.data = device.kind
        self.voltage_threshold.data = device.voltage_threshold
        self.device_id.data = device.device_id

    def to_model(self, device):
        device.config_id = self.config_id.data
        device.id = self.id.data
        device.name = self.name.data
        device.kind = self.kind.data
        device.voltage_threshold = self.voltage_threshold.data
        device.device_id = self.device_id.data

class DeviceWizardStep1(AbstractDeviceForm):
    name = StringField('Name', id = 'device_name', validators=[DataRequired(), Length(1, 64)])
    kind = SelectField('Kind', id = 'device_kind', choices = [(1, 'Keypad'), (2, 'Motion'), (3, 'Camera')])

    def __init__(self, formdata=_Auto, obj=None, prefix='', csrf_context=None,
                 secret_key=None, csrf_enabled=None, *args, **kwargs):
        super(DeviceWizardStep1, self).__init__(formdata, obj, prefix, csrf_context=csrf_context, *args, **kwargs)
        self.set_step(1)
        setattr(self.previous.flags, 'disabled', True)
        setattr(self.save.flags, 'disabled', True)
        setattr(self.save_and_new.flags, 'disabled', True)
    
class DeviceWizardStep2(AbstractDeviceForm):
    voltage_threshold = FloatField('Voltage Threshold', id = 'device_voltage')
    device_id = SelectField('Device ID', id = 'device_id')

    def __init__(self, formdata=_Auto, obj=None, prefix='', csrf_context=None,
                 secret_key=None, csrf_enabled=None, *args, **kwargs):
        super(DeviceWizardStep2, self).__init__(formdata, obj, prefix, csrf_context=csrf_context, *args, **kwargs)
        self.set_step(2)
        setattr(self.next.flags, 'disabled', True)

