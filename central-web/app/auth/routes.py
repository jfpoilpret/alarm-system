from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import SigninForm

from ..models import Account

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
