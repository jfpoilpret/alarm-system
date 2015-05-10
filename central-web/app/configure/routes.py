from json import loads
from re import compile
from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy import update

from app import db
from app.models import Configuration, Device
from app.configure.forms import ConfigForm, EditConfigForm, DeviceForm, EditDeviceForm, DevicesLocationForm
from app.configure import configure
from app.common import device_kinds, check_configurator, prepareMap,\
    extractSvgViewBox

@configure.route('/home')
@login_required
def home():
    all_configs = Configuration.query.all()
    return render_template('configure/home.html', configurations = all_configs)

#TODO refactor commin stuff between create and edit, also share same template
@configure.route('/edit_config/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_config(id):
    check_configurator()
    config = Configuration.query.get(id)
    #TODO show extra (readonly) field with latest upload filename
    configForm = EditConfigForm(prefix = 'config_', obj = config)
    if configForm.validate_on_submit():
        configForm.populate_obj(config)
        # If uploaded, read uploaded SVG file (XML)
        if configForm.map_area.has_file():
            map_area_field_data = configForm.map_area.data
            data = map_area_field_data.read().decode('utf-8')
            # Store XML SVG to DB
            config.map_area = data
            config.map_area_filename = map_area_field_data.filename
        db.session.add(config)
        db.session.commit()
        flash('Configuration ''%s''  has been saved' % config.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    return render_template('configure/edit_config.html', 
        config = config,
        configForm = configForm,
        deviceForm = None)

@configure.route('/create_config', methods = ['GET', 'POST'])
@login_required
def create_config():
    check_configurator()
    configForm = ConfigForm(prefix = 'config_')
    if configForm.validate_on_submit():
        config = Configuration()
        configForm.populate_obj(config)
        # If uploaded, read uploaded SVG file (XML)
        if configForm.map_area.has_file():
            map_area_field_data = configForm.map_area.data
            data = map_area_field_data.read().decode('utf-8')
            # Store XML SVG to DB
            config.map_area = data
            config.map_area_filename = map_area_field_data.filename
        db.session.add(config)
        db.session.commit()
        flash('New configuration ''%s''  has been created' % config.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    return render_template('configure/create_config.html', configForm = configForm)

DEVICEID_REGEX = compile('[0-9]+')
def find_device(config, device_id):
    id = int(DEVICEID_REGEX.findall(device_id)[0])
    return config.devices[id]

@configure.route('/edit_config_map/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_config_map(id):
    check_configurator()
    config = Configuration.query.get(id)
    configMapForm = DevicesLocationForm(prefix = 'config_')
    if configMapForm.validate_on_submit():
        # Get all modified devices locations as a JSON object
        new_locations = loads(configMapForm.devices_locations.data)
        dimensions = extractSvgViewBox(config)
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
        svgMap = prepareMap(config),
        configMapForm = configMapForm)

#TODO normally post only no?
# This method is called by javascript and is passed a JSON with all devices locations on the map
@configure.route('/save_devices_location/<int:id>', methods = ['GET', 'POST'])
@login_required
def save_devices_location(id):
    check_configurator()
    config = Configuration.query.get(id)
    #TODO
    flash('Modules locations for configuration ''%s''  have been saved' % config.name, 'success')
    return redirect(url_for('.edit_config_map', id = id))

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
    config = Configuration.query.get(device.config_id)
    device_config = device_kinds[device.kind]
    deviceForm = EditDeviceForm(prefix = 'device_', obj = device)
    init_device_id_choices(deviceForm, device_config)
    return validate_device_form(deviceForm, device.kind, device, config, False)

@configure.route('/create_device/<int:id>/<int:kind>', methods = ['GET', 'POST'])
@login_required
def create_device(id, kind):
    check_configurator()
    device = Device()
    device.config_id = id
    config = Configuration.query.get(id)
    device_config = device_kinds[kind]
    deviceForm = DeviceForm(prefix = 'device_', kind = kind, voltage_threshold = device_config.threshold)
    init_device_id_choices(deviceForm, device_config)
    return validate_device_form(deviceForm, kind, device, config, True)

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

def init_device_id_choices(deviceForm, device_config):
    choices = []
    for allowed_id in device_config.allowed_ids:
        choices.append((allowed_id, str(allowed_id)))
    deviceForm.device_id.choices = choices

def validate_device_form(deviceForm, kind, device, config, is_new):
    if deviceForm.validate_on_submit():
        deviceForm.populate_obj(device)
        db.session.add(device)
        db.session.commit()
        if is_new:
            flash('New module ''%s''  has been added' % device.name, 'success')
        else:
            flash('Module ''%s''  has been saved' % device.name, 'success')
        return redirect(url_for('.edit_config', id = config.id))
    configForm = EditConfigForm(prefix = 'config_', obj = config)
    return render_template('configure/edit_config.html', 
        id = config.id, 
        kind = kind, 
        config = config, 
        configForm = configForm, 
        deviceForm = deviceForm)
