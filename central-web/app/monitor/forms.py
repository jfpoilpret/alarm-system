from flask_wtf.form import Form
from wtforms.fields.core import DateField, SelectField
from wtforms.fields.simple import SubmitField, HiddenField
from wtforms.validators import Optional
from app.models import Alert, AlertType

class AlertsFilterForm(Form):
    latest_id = HiddenField()
    period_from = DateField('From', format='%d-%m-%Y', default = None, validators = [Optional()])
    period_to = DateField('to', format='%d-%m-%Y', default = None, validators = [Optional()])
    alert_level = SelectField('Level', coerce = int, default = 0, choices = [
        (0, 'All levels'), 
        (Alert.LEVEL_ALARM, 'Alarm only'), 
        (Alert.LEVEL_WARNING, 'Warning only'), 
        (Alert.LEVEL_INFO, 'Info only')])
    alert_type = SelectField('Type', coerce = int, default = 0, choices = [
        (0, 'All types'),
        (AlertType.LOCK, 'Lock only'),
        (AlertType.UNLOCK, 'Unlock only'),
        (AlertType.WRONG_LOCK_CODE, 'Bad lock code only'),
        (AlertType.DEVICE_VOLTAGE_UNDER_THRESHOLD, 'Voltage under threshold only'),
        (AlertType.DEVICE_NO_PING_FOR_TOO_LONG, 'No ping for too long only')])
    submit = SubmitField('Filter')

class HistoryClearForm(Form):
    clear_until = DateField('Until', format='%d-%m-%Y', default = None, validators = [Optional()])
    submit = SubmitField('Clear History')
