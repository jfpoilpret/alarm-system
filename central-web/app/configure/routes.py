from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import update

from app import db
from app.models import Configuration, Device
from app.configure.forms import ConfigForm, EditConfigForm, DeviceForm, EditDeviceForm
from app.configure import configure
from app.common import device_kinds

@configure.route('/home')
@login_required
def home():
    all_configs = Configuration.query.all()
    return render_template('configure/home.html', configurations=all_configs)

@configure.route('/edit_config/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_config(id):
    config = Configuration.query.get(id)
    configForm = EditConfigForm()
    if configForm.validate_on_submit():
        configForm.to_model(config)
        db.session.add(config)
        db.session.commit()
        flash('Configuration ''%s''  has been saved' % config.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    configForm.from_model(config)
    return render_template('configure/edit_config.html', 
        config = config,
        configForm = configForm,
        deviceForm = None)

@configure.route('/create_config', methods = ['GET', 'POST'])
@login_required
def create_config():
    form = ConfigForm()
    if form.validate_on_submit():
        config = Configuration()
        form.to_model(config)
        db.session.add(config)
        db.session.commit()
        flash('New configuration ''%s''  has been created' % config.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    return render_template('configure/create_config.html', form = form)

@configure.route('/delete_config/<int:id>')
@login_required
def delete_config(id):
    config = Configuration.query.get(id)
    if not config:
        flash('This configuration does not exist! It cannot be deleted!', 'danger')
    else:
        db.session.delete(config)
        db.session.commit()
        flash('Configuration has been deleted', 'success')
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

#TODO optimize models to directly get config from device
@configure.route('/edit_device/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_device(id):
    device = Device.query.get(id)
    config = Configuration.query.get(device.config_id)
    #TODO refactor to one function
    choices = []
    device_config = device_kinds[device.kind]
    for allowed_id in device_config.allowed_ids:
        choices.append((allowed_id, str(allowed_id)))
    deviceForm = EditDeviceForm(obj = device)
    deviceForm.device_id.choices = choices
    if deviceForm.validate_on_submit():
        deviceForm.populate_obj(device)
        db.session.add(device)
        db.session.commit()
        flash('Device ''%s''  has been saved' % device.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    configForm = EditConfigForm()
    configForm.from_model(config)
    return render_template('configure/edit_config.html', 
        id = config.id, 
        kind = device.kind, 
        config = config, 
        configForm = configForm, 
        deviceForm = deviceForm)
#    return render_template('configure/edit_device.html', id = config.id, kind = device.kind, config = config, form = form)

@configure.route('/create_device/<int:id>/<int:kind>', methods = ['GET', 'POST'])
@login_required
def create_device(id, kind):
    config = Configuration.query.get(id)
    choices = []
    device_config = device_kinds[kind]
    for allowed_id in device_config.allowed_ids:
        choices.append((allowed_id, str(allowed_id)))
    form = DeviceForm(kind = kind, voltage_threshold = device_config.threshold)
    form.device_id.choices = choices
    if form.validate_on_submit():
        device = Device()
        device.config_id = id
        form.populate_obj(device)
        db.session.add(device)
        db.session.commit()
        flash('New device ''%s''  has been added' % device.name, 'success')
        return redirect(url_for('.edit_config', id = id))
    print('create_device() device_id = %s' % form.device_id.data)
    return render_template('configure/edit_device.html', id = id, kind = kind, config = config, form = form)

@configure.route('/delete_device/<int:id>')
@login_required
def delete_device(id):
    device = Device.query.get(id)
    if not device:
        flash('This module does not exist! It cannot be deleted!', 'danger')
    else:
        db.session.delete(device)
        db.session.commit()
        flash('Module has been deleted', 'success')
        return redirect(url_for('.edit_config', id = device.config_id))
    return redirect(url_for('.home'))

