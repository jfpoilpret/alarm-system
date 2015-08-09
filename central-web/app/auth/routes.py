from flask import flash, redirect, render_template, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.auth.forms import SigninForm

from app.models import Account
from app.auth.forms import ProfileForm, PasswordForm
from app import db

def render_signin_page(signin_form = None):
    if not signin_form:
        signin_form = SigninForm(prefix = 'signin_', formdata = None)
    return render_template('auth/signin.html', signin_form = signin_form)

@auth.route('/signin', methods=['POST'])
def signin():
    signin_form = SigninForm(prefix = 'signin_')
    if signin_form.validate_on_submit():
        user = Account.query.filter_by(username = signin_form.username.data).first()
        if user and user.verify_password(signin_form.password.data):
            login_user(user)
            if user.is_configurator():
                return redirect(url_for('configure.home'))
            else:
                return redirect(url_for('monitor.home'))
        flash('Invalid username or password.', 'warning')
    return render_signin_page(signin_form = signin_form)

@auth.route('/login')
def login():
    return render_signin_page()

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

@auth.route('/get_profile')
@login_required
def get_profile():
    profile_form = ProfileForm(prefix = 'profile_', obj = current_user)
    return render_template('auth/dialog_profile.html', 
        profile_form = profile_form)

@auth.route('/save_profile', methods = ['POST'])
@login_required
def save_profile():
    profile_form = ProfileForm(prefix = 'profile_', obj = current_user)
    if profile_form.validate_on_submit():
        profile_form.populate_obj(current_user)
        db.session.add(current_user)
        db.session.commit()
        return jsonify(
            result = 'OK',
            username = current_user.username,
            fullname = current_user.fullname,
            flash = render_template('flash_messages.html', message = 'Your profile has been saved', category = 'success'))
    return jsonify(
        result = 'ERROR',
        form = render_template('auth/dialog_profile.html', profile_form = profile_form))

@auth.route('/get_password')
@login_required
def get_password():
    password_form = PasswordForm(prefix = 'password_')
    return render_template('auth/dialog_password.html', password_form = password_form)

@auth.route('/save_password', methods = ['POST'])
@login_required
def save_password():
    password_form = PasswordForm(prefix = 'password_')
    if password_form.validate_on_submit():
        # check both passwords are the same
        pw1 = password_form.password.data
        pw2 = password_form.repeat_password.data
        if pw1 == pw2:
            current_user.password = pw1
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been changed', 'success')
            return jsonify(
                result = 'OK',
                flash = render_template('flash_messages.html', message = 'Your password has been changed', category = 'success'))
        else:
            #TODO replace flash with field error!!!
            return jsonify(
                result = 'ERROR',
                form = None,
                flash = render_template('flash_messages.html', message = 'Please ensure you typed the same password twice!', category = 'warning'))
    return jsonify(
        result = 'ERROR',
        flash = '',
        form = render_template('auth/dialog_password.html', password_form = password_form))
