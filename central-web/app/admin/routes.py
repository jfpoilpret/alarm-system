from flask import abort, jsonify, render_template, request
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
    return render_template('admin/users.html', is_new = True, user_form = NewUserForm(prefix = 'user_'))

@admin.route('/get_users_list')
@login_required
def get_users_list():
    check_admin()
    users = Account.query.order_by(Account.username).all()
    return render_template('admin/all_user_rows.html', users = users)

@admin.route('/get_user/<int:id>')
@login_required
def get_user(id):
    check_admin()
    user = Account.query.get_or_404(id)
    user_form = EditUserForm(prefix = 'user_', obj = user)
    return render_template('admin/dialog_user.html', is_new = False, user_form = user_form)

@admin.route('/save_user', methods = ['POST'])
@login_required
def save_user():
    check_admin()
    id = int(request.form.get('user_id'))
    if id:
        # Existing user
        user = Account.query.get_or_404(id)
        user_form = EditUserForm(prefix = 'user_', obj = user)
        success = 'User ''%s'' has been saved'
    else:
        # New user
        user = Account()
        user_form = NewUserForm(prefix = 'user_', obj = user)
        success = 'New user ''%s'' has been created'
    # Try to validate form first
    if user_form.validate():
        # Temporarily store id & filename to restore them after they are overwritten by populate_obj
        id = user.id
        user_form.populate_obj(user)
        user.id = id
        db.session.add(user)
        db.session.commit()
        message = success % user.username
        return jsonify(
            result = 'OK',
            flash = render_template('flash_messages.html', message = message, category = 'success'),
            users = get_users_list())
    else:
        return jsonify(
            result = 'ERROR',
            form = render_template('admin/dialog_user.html', is_new = False, user_form = user_form))

@admin.route('/delete_user/<int:id>', methods = ['POST'])
@login_required
def delete_user(id):
    check_admin()
    if current_user.id == id:
        abort(400, message = 'You cannot remove yourself!')
    user = Account.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    message = 'User ''%s''  has been removed' % user.username
    return jsonify(
        result = 'OK',
        flash = render_template('flash_messages.html', message = message, category = 'success'),
        users = get_users_list())

@admin.route('/reset_user_password/<int:id>')
@login_required
def reset_user_password(id):
    check_admin()
    user = Account.query.get_or_404(id)
    user.password = ''
    db.session.add(user)
    db.session.commit()
    message = 'User ''%s''  password has been reset' % user.username
    return jsonify(
        result = 'OK',
        flash = render_template('flash_messages.html', message = message, category = 'success'))
