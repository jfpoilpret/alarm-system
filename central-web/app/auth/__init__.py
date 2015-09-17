#TODO remove package and integrate somewhere else...
from flask import g
from flask_httpauth import HTTPBasicAuth

from ..models import Account

auth = HTTPBasicAuth()

@auth.verify_password
def verify_token(user_or_token, password):
    print('verify_token(%s, %s) #1' % (user_or_token, password))
    user = Account.verify_auth_token(user_or_token)
    print('verify_token #2 user = %s' % str(user))
    if not user:
        print('verify_token #3')
        user = Account.query.filter_by(username = user_or_token).first()
        print('verify_token #4 user = %s' % str(user))
    g.user = user
    if not user:
        return False
    return True
