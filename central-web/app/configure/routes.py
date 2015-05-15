from json import loads
from re import compile
from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import update

from app import db
from app.models import Configuration, Device
from app.configure.forms import NewConfigForm, EditConfigForm, NewDeviceForm, EditDeviceForm, DevicesLocationForm
from app.configure import configure
from app.common import device_kinds, check_configurator, prepare_map_for_config, extract_viewbox_from_config

@configure.route('/home')
@login_required
def home():
    all_configs = Configuration.query.all()
    return render_template('configure/home.html', configurations = all_configs)

@configure.route('/edit_config/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_config(id):
    check_configurator()
    config = Configuration.query.get(id)
    return check_config_submit(
        config_form = EditConfigForm(prefix = 'config_', obj = config),
        config = config, 
        is_new = False)

@configure.route('/create_config', methods = ['GET', 'POST'])
@login_required
def create_config():
    check_configurator()
    return check_config_submit(
        config_form = NewConfigForm(prefix = 'config_'), 
        config = Configuration(), 
        is_new = True)

# Common handling of config creation/edition requests
def check_config_submit(config_form, config, is_new):
    if config_form.validate_on_submit():
        config_form.populate_obj(config)
        # If uploaded, read uploaded SVG file (XML)
        if config_form.map_area_file.has_file():
            map_area_field_data = config_form.map_area_file.data
            data = map_area_field_data.read().decode('utf-8')
            # Store XML SVG to DB
            config.map_area = data
            config.map_area_filename = map_area_field_data.filename
        db.session.add(config)
        db.session.commit()
        if is_new:
            flash('New configuration ''%s''  has been created' % config.name, 'success')
        else:
            flash('Configuration ''%s''  has been saved' % config.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    if is_new:
        return render_template('configure/create_config.html', 
            config_form = config_form,
            url_return = url_for('.home'))
    else:
        return render_template('configure/edit_config.html', 
            config = config,
            config_form = config_form,
            device_form = None,
            url_return = url_for('.home'))

DEVICEID_REGEX = compile('[0-9]+')
def find_device(config, device_id):
    id = int(DEVICEID_REGEX.findall(device_id)[0])
    return config.devices[id]

@configure.route('/edit_config_map/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_config_map(id):
    check_configurator()
    config = Configuration.query.get(id)
    config_map_form = DevicesLocationForm(prefix = 'config_')
    if config_map_form.validate_on_submit():
        # Get all modified devices locations as a JSON object
        new_locations = loads(config_map_form.devices_locations.data)
        dimensions = extract_viewbox_from_config(config)
        for device_id, location in new_locations.items():
            # extract device
            device = find_device(config, device_id)
            # interpret all devices locations (as ratios)
            device.location_x = (location['x'] - dimensions[0]) / dimensions[2]
            device.location_y = (location['y'] - dimensions[1]) / dimensions[3]
            db.session.add(device)
        db.session.commit()
        flash('New devices locations for ''%s''  have been saved' % config.name, 'success')
        return redirect(url_for('.edit_config_map', id = id))
    return render_template('configure/edit_config_map.html', 
        config = config,
        svg_map = prepare_map_for_config(config),
        config_map_form = config_map_form)

@configure.route('/delete_config/<int:id>')
@login_required
def delete_config(id):
    check_configurator()
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
    check_configurator()
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
    check_configurator()
    device = Device.query.get(id)
    device_config = device_kinds[device.kind]
    device_form = EditDeviceForm(prefix = 'device_', obj = device)
    init_device_id_choices(device_form, device_config)
    return validate_device_form(device_form, device, False)

@configure.route('/create_device/<int:id>/<int:kind>', methods = ['GET', 'POST'])
@login_required
def create_device(id, kind):
    check_configurator()
    device_config = device_kinds[kind]
    device = Device(config_id = id, kind = kind, voltage_threshold = device_config.threshold)
    device_form = NewDeviceForm(prefix = 'device_', obj = device)
    init_device_id_choices(device_form, device_config)
    return validate_device_form(device_form, device, True)

@configure.route('/delete_device/<int:id>')
@login_required
def delete_device(id):
    check_configurator()
    device = Device.query.get(id)
    if not device:
        flash('This module does not exist! It cannot be deleted!', 'danger')
    else:
        db.session.delete(device)
        db.session.commit()
        flash('Module has been deleted', 'success')
        return redirect(url_for('.edit_config', id = device.config_id))
    return redirect(url_for('.home'))

def init_device_id_choices(device_form, device_config):
    choices = []
    for allowed_id in device_config.allowed_ids:
        choices.append((allowed_id, str(allowed_id)))
    device_form.device_id.choices = choices

def validate_device_form(device_form, device, is_new):
    config = Configuration.query.get(device.config_id)
    if device_form.validate_on_submit():
        device_form.populate_obj(device)
        db.session.add(device)
        db.session.commit()
        if is_new:
            flash('New module ''%s''  has been added' % device.name, 'success')
        else:
            flash('Module ''%s''  has been saved' % device.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    config_form = EditConfigForm(prefix = 'config_', obj = config)
    return render_template('configure/edit_config.html', 
        id = config.id, 
        kind = device.kind, 
        config = config, 
        config_form = config_form, 
        device_form = device_form)
