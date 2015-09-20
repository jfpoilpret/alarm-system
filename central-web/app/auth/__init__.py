#TODO remove package and integrate somewhere else...
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from ..models import Account

# Note: we use a "Dummy" scheme to avoid browser popping up its own dialog when receiving 401
auth = HTTPBasicAuth(scheme = 'Dummy', realm = 'None')

@auth.error_handler
def auth_error_handler():
    res = jsonify(message = 'Invalid credentials')
    res.status_code = 401
    return res

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
