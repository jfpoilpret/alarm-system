from flask_wtf.form import Form
from wtforms.fields.core import DateField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import Optional

class AlertsFilterForm(Form):
    period_from = DateField('From', format='%d-%m-%Y', default = None, validators=[Optional()])
    period_to = DateField('to', format='%d-%m-%Y', default = None, validators=[Optional()])
    alert_level = SelectField('Level', coerce = int, default = 0)
    alert_type = SelectField('Type', coerce = int, default = 0)
    submit = SubmitField('Filter')

