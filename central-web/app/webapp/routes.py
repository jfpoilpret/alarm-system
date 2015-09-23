# encoding: utf-8

from flask import render_template, request
from app.webapp import webapp

@webapp.route('/signin')
def signin():
    return render_template('skeleton.html')

@webapp.route('/page')
def page():
    return render_template(request.args['name'])
