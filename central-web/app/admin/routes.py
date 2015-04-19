from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import admin

from .. import db
from ..models import Account

@admin.route('/users')
@login_required
def users():
    users = Account.query.order_by(Account.username).all()
    return render_template('admin/users.html', users = users)

@admin.route('/delete_user/<int:userid>')
@login_required
def delete_user(userid):
    if not current_user.is_admin:
        abort(401, message = 'Only admin can remove a user!')
    if current_user.id == userid:
        abort(400, message = 'You cannot remove yourself!')
    user = Account.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('.users'))
