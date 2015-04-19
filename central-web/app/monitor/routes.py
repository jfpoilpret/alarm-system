from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from . import monitor

from ..models import Configuration

@monitor.route('/home')
@login_required
def home():
    current_config = Configuration.query.filter_by(current=True).first()
    return render_template('monitor/home.html', configuration=current_config)
