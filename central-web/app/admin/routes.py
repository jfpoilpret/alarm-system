from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app.admin import admin

from app import db
from app.models import Account
from app.common import check_admin
from app.admin.forms import EditUserForm, NewUserForm

@admin.route('/users')
@login_required
def users():
    check_admin()
    users = Account.query.order_by(Account.username).all()
    return render_template('admin/users.html', users = users)

@admin.route('/edit_user/<int:userid>', methods = ['GET', 'POST'])
@login_required
def edit_user(userid):
    check_admin()
    user = Account.query.get(userid)
    userForm = EditUserForm(prefix = 'user_', obj = user)
    if userForm.validate_on_submit():
        userForm.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('User ''%s''  has been saved' % user.username, 'success')
        return redirect(url_for('.users'))
    return render_template('admin/edit_user.html', userForm = userForm)

@admin.route('/create_user', methods = ['GET', 'POST'])
@login_required
def create_user():
    check_admin()
    userForm = NewUserForm(prefix = 'user_')
    if userForm.validate_on_submit():
        user = Account()
        userForm.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('User ''%s''  has been created' % user.username, 'success')
        return redirect(url_for('.users'))
    return render_template('admin/create_user.html', userForm = userForm)

@admin.route('/delete_user/<int:userid>')
@login_required
def delete_user(userid):
    check_admin()
    if current_user.id == userid:
        abort(400, message = 'You cannot remove yourself!')
    user = Account.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    flash('User ''%s''  has been removed' % user.username, 'success')
    return redirect(url_for('.users'))


@admin.route('/reset_user_password/<int:userid>')
@login_required
def reset_user_password(userid):
    check_admin()
    user = Account.query.get(userid)
    user.password = ''
    db.session.add(user)
    db.session.commit()
    flash('User ''%s''  password has been reset' % user.username, 'success')
    return redirect(url_for('.users'))
