from flask import render_template, request
from app.webapp import webapp
from app import auth

# TODO one unprotected route (for signin only) and one protected route for all other features

@webapp.route('/signin')
def signin():
    return render_template('skeleton.html')

@webapp.route('/page')
# @auth.login_required
def page():
    print('page(%s)' % request.args['name'])
    return render_template(request.args['name'])
