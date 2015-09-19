#TODO remove package and integrate somewhere else...
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from ..models import Account

auth = HTTPBasicAuth()

# Hack to ensure HTTPBasicAuth doesn't add 'WWW-Authenticate' header and thus avoids browser popups
def auth_error_handler():
    res = jsonify(message = 'Invalid credentials')
    res.status_code = 401
    return res

auth.auth_error_callback = auth_error_handler

@auth.verify_password
def verify_token(user_or_token, password):
    user = Account.verify_auth_token(user_or_token)
    if not user:
        g.token = None
        user = Account.query.filter_by(username = user_or_token).first()
        if user and not user.verify_password(password):
            user = None
    else:
        g.token = user_or_token
    g.user = user
    print('verify_token user = %s' % str(user))
    return (user is not None)
