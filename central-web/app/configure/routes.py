from flask import g, render_template

from app.configure import configure
from app.auth import auth

@configure.route('/home')
@auth.login_required
def home():
    return render_template('configure/home.html', current_user = g.user)
