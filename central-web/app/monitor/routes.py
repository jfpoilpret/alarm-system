from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from . import monitor

from app.models import Configuration
from app.common import check_alarm_setter, prepare_map_for_monitoring
from app import db

@monitor.route('/home')
@login_required
def home():
    current_config = Configuration.query.filter_by(current=True).first()
    return render_template('monitor/home.html', 
        configuration = current_config,
        svg_map = prepare_map_for_monitoring(current_config))

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
