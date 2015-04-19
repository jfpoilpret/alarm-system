from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import update

from app import db
from app.models import Configuration, Device
from app.configure.forms import ConfigForm, EditConfigForm, DeviceForm
from app.configure import configure

@configure.route('/home')
@login_required
def home():
    all_configs = Configuration.query.all()
    return render_template('configure/home.html', configurations=all_configs)

@configure.route('/edit_config/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_config(id):
    config = Configuration.query.get(id)
    form = EditConfigForm()
    if form.validate_on_submit():
        form.to_model(config)
        db.session.add(config)
        db.session.commit()
        flash('Configuration ''%s''  has been saved' % config.name)
        return redirect(url_for('.edit_config', id = config.id))
    form.from_model(config)
    return render_template('configure/edit_config.html', 
        config = config,
        form = form)

@configure.route('/create_config', methods = ['GET', 'POST'])
@login_required
def create_config():
    form = ConfigForm()
    if form.validate_on_submit():
        config = Configuration()
        form.to_model(config)
        db.session.add(config)
        db.session.commit()
        flash('New configuration ''%s''  has been created' % config.name)
        return redirect(url_for('.edit_config', id = config.id))
    return render_template('configure/create_config.html', form = form)

@configure.route('/delete_config/<int:id>')
@login_required
def delete_config(id):
    config = Configuration.query.get(id)
    if not config:
        flash('This configuration does not exist! It cannot be deleted!')
    else:
        db.session.delete(config)
        db.session.commit()
        flash('Configuration has been deleted')
    return redirect(url_for('.home'))

@configure.route('/set_current_config/<int:id>')
@login_required
def set_current_config(id):
    config = Configuration.query.get(id)
    if not config.current:
        db.session.execute(update(Configuration.__table__).values(current = False))
        config.current = True
        db.session.add(config)
        db.session.commit()
    return redirect(url_for('.home'))

#TODO create device, edit device
@configure.route('/create_device/<int:id>', methods = ['POST'])
@login_required
def create_device(id):
    config = Configuration.query.get(id)
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device()
        device.config_id = id
        form.to_model(device)
        db.session.add(config)
        db.session.commit()
        flash('New device ''%s''  has been added' % device.name)
        return redirect(url_for('.edit_config', id = id))
    return render_template('configure/create_config.html', form = form)
