from datetime import datetime
from time import time
from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import monitor

from app.models import Configuration, Alert, AlertType
from app.common import check_alarm_setter, prepare_map_for_monitoring
from app import db
from app.monitor.forms import AlertsFilterForm

#TODO split in two functions: general home + AJAX for alert list refresh (with filters)
@monitor.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    # Find current configuration
    #FIXME handle situation where there is no current configuration setup yet!
    current_config = Configuration.query.filter_by(current = True).first()
    # Check alerts filter form
    filter_form = AlertsFilterForm(prefix = 'alert_filter_')
    # Setup all dropdown in form
    filter_form.alert_level.choices = [
        (0, 'All levels'), 
        (Alert.LEVEL_ALARM, 'Alarm only'), 
        (Alert.LEVEL_WARNING, 'Warning only'), 
        (Alert.LEVEL_INFO, 'Info only') ]
    filter_form.alert_type.choices = [
        (0, 'All types'),
        (AlertType.LOCK, 'Lock only'),
        (AlertType.UNLOCK, 'Unlock only'),
        (AlertType.WRONG_LOCK_CODE, 'Bad lock code only'),
        (AlertType.DEVICE_VOLTAGE_UNDER_THRESHOLD, 'Voltage under threshold only'),
        (AlertType.DEVICE_NO_PING_FOR_TOO_LONG, 'No ping for too long only') ]
    # Set default active tab
    if filter_form.is_submitted():
        active_tab = 'alerts'
    else:
        active_tab = 'maps'
    if filter_form.validate_on_submit():
        alerts = filter_alerts(current_config.id, filter_form)
    else:
        # Limit to last 30 days by default
        limit = datetime.fromtimestamp(time() - 30 * 24 * 3600)
        filter_form.period_from.data = limit
        alerts = Alert.query.filter_by(config_id = current_config.id).filter(Alert.when >= limit).order_by(Alert.when.desc()).all()
    return render_template('monitor/home.html', 
        configuration = current_config,
        filter_form = filter_form,
        alerts = alerts,
        active_tab = active_tab,
        svg_map = prepare_map_for_monitoring(current_config))

def filter_alerts(config_id, filter_form):
    query = Alert.query.filter_by(config_id = config_id)
    if filter_form.period_from.data:
        query = query.filter(Alert.when >= filter_form.period_from.data)
    if filter_form.period_to.data:
        query = query.filter(Alert.when <= filter_form.period_to.data)
    if filter_form.alert_level.data and filter_form.alert_level.data != 0:
        query = query.filter_by(level = filter_form.alert_level.data)
    if filter_form.alert_type.data and filter_form.alert_type.data != 0:
        query = query.filter_by(alert_type = filter_form.alert_type.data)
    return query.order_by(Alert.when.desc()).all()
    
@monitor.route('/activate')
@login_required
def activate_config():
    return set_config_active(True)

@monitor.route('/deactivate')
@login_required
def deactivate_config():
    return set_config_active(False)

def set_config_active(active):
    check_alarm_setter()
    current_config = Configuration.query.filter_by(current=True).first()
    if current_config.active != active:
        current_config.active = active
        db.session.add(current_config)
        db.session.commit()
        # Actually activate/deactivate the alarm system
        from app.monitor.monitoring import MonitoringManager
        if active:
            MonitoringManager.instance.activate(current_config)
        else:
            MonitoringManager.instance.deactivate()
    return redirect(url_for('.home'))
