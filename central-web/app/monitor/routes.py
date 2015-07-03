from datetime import datetime
from time import time
from flask import render_template, request, jsonify
from flask_login import login_required

from . import monitor

from app.models import Configuration, Alert
from app.common import check_alarm_setter, pre_check, prepare_map_for_monitoring
from app import db
from app.monitor.forms import AlertsFilterForm, HistoryClearForm
from app.monitor.monitoring import MonitoringManager

@monitor.route('/home', methods = ['GET'])
@login_required
def home():
    # Find current configuration
    #FIXME handle situation where there is no current configuration setup yet!
    current_config = Configuration.query.filter_by(current = True).first()
    # Set default active tab
    active_tab = request.args.get('tab', 'tab_map')
    # Setup filter form
    filter_form = AlertsFilterForm(prefix = 'alert_filter_', latest_id = '-1')
    # Limit to last 30 days by default
    limit = datetime.fromtimestamp(time() - 30 * 24 * 3600)
    filter_form.period_from.data = limit
    return render_template('monitor/home.html', 
        configuration = current_config,
        filter_form = filter_form,
        history_clear_form = HistoryClearForm(prefix = 'history_clear_'),
        active_tab = active_tab,
        svg_map = prepare_map_for_monitoring(current_config))

def filter_alerts(config_id, filter_form, limit = False, max_rows = 100):
    query = Alert.query.filter_by(config_id = config_id)
    if limit:
        latest_id = int(filter_form.latest_id.data)
        query = query.filter(Alert.id > latest_id)
    if filter_form.period_from.data:
        query = query.filter(Alert.when >= filter_form.period_from.data)
    if filter_form.period_to.data:
        query = query.filter(Alert.when <= filter_form.period_to.data)
    if filter_form.alert_level.data and filter_form.alert_level.data != 0:
        query = query.filter_by(level = filter_form.alert_level.data)
    if filter_form.alert_type.data and filter_form.alert_type.data != 0:
        query = query.filter_by(alert_type = filter_form.alert_type.data)
    # Limit number of retrieved records
    query = query.order_by(Alert.when.desc())
    if max_rows:
        query = query.limit(max_rows)
    return query.all()
    
@monitor.route('/pre_refresh_alerts', methods = ['POST'])
@login_required
def pre_refresh_alerts():
    # Check alerts filter form
    return pre_check(AlertsFilterForm(prefix = 'alert_filter_'))

@monitor.route('/refresh_alerts', methods = ['POST'])
@login_required
def refresh_alerts():
    # Find current configuration
    current_config = Configuration.query.filter_by(current = True).first()
    # Check alerts filter form
    filter_form = AlertsFilterForm(prefix = 'alert_filter_')
    alerts = filter_alerts(current_config.id, filter_form, limit = True)
    latest_id = int(filter_form.latest_id.data)
    alerts_display = []
    # Prepare rendering of new alerts so they are ready to integrate into the DOM on JS side
    if alerts:
        latest_id = alerts[0].id
        alerts_display = [render_template('monitor/alerts.html', alert = alert) for alert in alerts]
    return jsonify(alerts = alerts_display, latest_id = latest_id)

def create_device_for_refresh(device, now):
    if device.latest_voltage_level and device.source.voltage_threshold:
        voltage_rate = device.latest_voltage_level / device.source.voltage_threshold
        if voltage_rate >= 1.05:
            voltage_alert = 0
        elif voltage_rate >= 1.0:
            voltage_alert = 1
        elif voltage_rate >= 0.9:
            voltage_alert = 2
        else:
            voltage_alert = 3
        if device.latest_ping > now - 5.0:
            ping_alert = 0
        elif device.latest_ping > now - 10.0:
            ping_alert = 1
        elif device.latest_ping > now - 30.0:
            ping_alert = 2
        else:
            ping_alert = 3
    else:
        voltage_alert = 0
        ping_alert = 0
    
    return {
        'id': device.source.device_id,
        'voltage_threshold': device.source.voltage_threshold,
        'latest_voltage': device.latest_voltage_level,
        'latest_ping': datetime.fromtimestamp(device.latest_ping).strftime('%d.%m.%Y %H:%M:%S'),
        'time_since_latest_ping': now - device.latest_ping,
        'voltage_alert': voltage_alert,
        'ping_alert': ping_alert
    }

@monitor.route('/refresh_devices', methods = ['POST'])
@login_required
def refresh_devices():
    # Get list of all devices in current configuration and prepare for return to UI
    now = time()
    devices = [create_device_for_refresh(device, now) for device in MonitoringManager.instance.get_devices().values()]
    return jsonify(devices = devices)

@monitor.route('/load_history_page/<int:page>', methods = ['GET'])
@login_required
def load_history_page(page):
    # Find current configuration
    current_config = Configuration.query.filter_by(current = True).first()
    # Check alerts filter form
    query = Alert.query.filter_by(config_id = current_config.id).order_by(Alert.when.desc())
    pagination = query.paginate(page, error_out = False)
    # Prepare rendering of new alerts so they are ready to integrate into the DOM on JS side
    alerts_display = [render_template('monitor/alerts.html', alert = alert) for alert in pagination.items]
    # Prepare rendering of pagination buttons
    pagination_display = render_template('monitor/history_pagination.html', pagination = pagination)
    return jsonify(alerts = alerts_display, pagination = pagination_display)

@monitor.route('/pre_clear_history', methods = ['POST'])
@login_required
def pre_clear_history():
    return pre_check(HistoryClearForm(prefix = 'history_clear_'))

@monitor.route('/clear_history', methods = ['POST'])
@login_required
def clear_history():
    check_alarm_setter()
    # Find current configuration
    current_config = Configuration.query.filter_by(current = True).first()
    # Delete all alerts for current configuration
    history_clear_form =  HistoryClearForm(prefix = 'history_clear_')
    query = Alert.query.filter_by(config_id = current_config.id)
    if history_clear_form.clear_until.data:
        query = query.filter(Alert.when <= history_clear_form.clear_until.data)
    query.delete(synchronize_session = False)
    db.session.commit()
    return ''

@monitor.route('/activate_config', methods = ['POST'])
@login_required
def activate_config():
    return set_config_active(True)

@monitor.route('/deactivate_config', methods=['POST'])
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
    return ''
