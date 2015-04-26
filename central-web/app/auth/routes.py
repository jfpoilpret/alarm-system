from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.auth.forms import SigninForm

from app.models import Account
from app.auth.forms import ProfileForm, PasswordForm
from app import db

def renderSignInPage(signinForm = None):
    if not signinForm:
        signinForm = SigninForm(prefix = 'signin_', formdata = None)
    return render_template('auth/signin.html', 
        signin = signinForm, 
        signinUrl = url_for('.signin'))

@auth.route('/signin', methods=['POST'])
def signin():
    signinForm = SigninForm(prefix = 'signin_')
    if signinForm.validate_on_submit():
        user = Account.query.filter_by(username = signinForm.username.data).first()
        if user and user.verify_password(signinForm.password.data):
            login_user(user)
            return redirect(url_for('configure.home'))
        flash('Invalid username or password.', 'warning')
    return renderSignInPage(signinForm = signinForm)

@auth.route('/login')
def login():
    return renderSignInPage()

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profileForm = ProfileForm(prefix = 'profile_', obj = current_user)
    if profileForm.validate_on_submit():
        profileForm.populate_obj(current_user)
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been saved', 'success')
        return redirect(url_for('configure.home'))
    return render_template('auth/profile.html', profileForm = profileForm)

@auth.route('/password', methods=['GET', 'POST'])
@login_required
def change_password():
    passwordForm = PasswordForm(prefix = 'password_')
    if passwordForm.validate_on_submit():
        # check both passwords are the same
        pw1 = passwordForm.password.data
        pw2 = passwordForm.repeat_password.data
        if pw1 == pw2:
            current_user.password = pw1
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been changed', 'success')
            return redirect(url_for('configure.home'))
        else:
            flash('Please ensure you typed the same password twice!', 'warning')
    return render_template('auth/password.html', passwordForm = passwordForm)
