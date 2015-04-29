from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from . import monitor

from app.models import Configuration
from app.common import check_alarm_setter
from app import db

@monitor.route('/home')
@login_required
def home():
    current_config = Configuration.query.filter_by(current=True).first()
    return render_template('monitor/home.html', configuration=current_config)

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
        #TODO need to REALLY activate/deactivate the alarm system somehow (TBD)
        db.session.add(current_config)
        db.session.commit()
    return redirect(url_for('.home'))
