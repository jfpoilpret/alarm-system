from flask import g, render_template

from app.monitor import monitor
from app.auth import auth

@monitor.route('/home')
@auth.login_required
def home():
    return render_template('monitor/monitoring.html', current_user = g.user)

#TODO does not belong here...
@monitor.route('/signin')
def signin():
#     return render_template('monitor/main_login.html', current_user = None)
    return render_template('skeleton.html')

