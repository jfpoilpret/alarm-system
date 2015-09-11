from flask import g, render_template
from app.admin import admin
from app.auth import auth

from app.common import check_admin

@admin.route('/users')
@auth.login_required
def users():
    check_admin()
    return render_template('admin/users.html', current_user = g.user)
