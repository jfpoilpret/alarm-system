from json import loads
from re import compile
from flask import flash, jsonify, redirect, render_template, request, url_for
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
    return render_template('configure/home.html', config_form = NewConfigForm(prefix = 'config_'))

@configure.route('/get_configs_list')
@login_required
def get_configs_list():
    #TODO order by name!!!
    all_configs = Configuration.query.all()
    return render_template('configure/all_config_rows.html', configurations = all_configs)

@configure.route('/get_config/<int:id>')
@login_required
def get_config(id):
    config = Configuration.query.get_or_404(id)
    config_form = EditConfigForm(prefix = 'config_', obj = config)
    device_form = NewDeviceForm(prefix = 'device_')
    return render_template('configure/dialog_edit_config.html', 
        config = config, config_form = config_form, device_form = device_form)

@configure.route('/save_config', methods = ['POST'])
@login_required
def save_config():
    check_configurator()
    id = request.form.get('config_id')
    if id:
        # Existing configuration
        config = Configuration.query.get_or_404(int(id))
        config_form = EditConfigForm(prefix = 'config_', obj = config)
        device_form = NewDeviceForm(prefix = 'device_')
        template = 'configure/dialog_edit_config.html'
        success = 'Configuration ''%s'' has been saved'
    else:
        # New configuration
        config = Configuration()
        config_form = NewConfigForm(prefix = 'config_', obj = config)
        device_form = None
        template = 'configure/dialog_create_config.html'
        success = 'New configuration ''%s'' has been created'
    # Try to validate form first
    if config_form.validate():
        # Temporarily store id & filename to restore them after they are overwritten by populate_obj
        id = config.id
        filename = config.map_area_filename
        config_form.populate_obj(config)
        config.id = id
        config.map_area_filename = filename
        # If uploaded, read uploaded SVG file (XML)
        if config_form.map_area_file.has_file():
            map_area_field_data = config_form.map_area_file.data
            data = map_area_field_data.read().decode('utf-8')
            # Store XML SVG to DB
            config.map_area = data
            config.map_area_filename = map_area_field_data.filename
        db.session.add(config)
        db.session.commit()
        message = success % config.name
        return jsonify(
            result = 'OK',
            flash = render_template('flash_messages.html', message = message, category = 'success'),
            configs = get_configs_list())
    else:
        return jsonify(
            result = 'ERROR',
            form = render_template(template, 
                config = config, config_form = config_form, device_form = device_form))

DEVICEID_REGEX = compile('[0-9]+')
def find_device(config, device_id):
    id = int(DEVICEID_REGEX.findall(device_id)[0])
    return config.devices[id]

@configure.route('/edit_config_map/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_config_map(id):
    check_configurator()
    config = Configuration.query.get(id)
    if not config.map_area:
        flash('Configuration ''%s'' has no Monitored Zone Map set yet!' % config.name, 'warning')
        return redirect(url_for('.home'))
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

@configure.route('/delete_config/<int:id>', methods = ['POST'])
@login_required
def delete_config(id):
    check_configurator()
    config = Configuration.query.get_or_404(id)
    #TODO pass flash messages through JSON...
    if not config:
        pass
#        flash('This configuration does not exist! It cannot be deleted!', 'danger')
    else:
        db.session.delete(config)
        db.session.commit()
#        flash('Configuration has been deleted', 'success')
    return get_configs_list()

#TODO if previously current config is active, deactivate it first!
@configure.route('/set_current_config/<int:id>', methods = ['POST'])
@login_required
def set_current_config(id):
    check_configurator()
    config = Configuration.query.get_or_404(id)
    if not config.current:
        db.session.execute(update(Configuration.__table__).values(current = False))
        config.current = True
        db.session.add(config)
        db.session.commit()
    return get_configs_list()

@configure.route('/get_devices/<int:id>')
@login_required
def get_devices(id):
    config = Configuration.query.get_or_404(id)
    return render_template('configure/all_module_rows.html', config = config)

@configure.route('/get_new_device_form/<int:id>/<int:kind>')
@login_required
def get_new_device_form(id, kind):
    check_configurator()
    device_config = device_kinds[kind]
    device_form = NewDeviceForm(prefix = 'device_', 
        id = 0, config_id = id, kind = kind, voltage_threshold = device_config.threshold)
    init_device_id_choices(device_form, device_config)
    return render_template('configure/edit_device_form.html', device_form = device_form)

@configure.route('/get_edit_device_form/<int:id>')
@login_required
def get_edit_device_form(id):
    check_configurator()
    device = Device.query.get_or_404(id)
    device_config = device_kinds[device.kind]
    device_form = EditDeviceForm(prefix = 'device_', obj = device)
    init_device_id_choices(device_form, device_config)
    return render_template('configure/edit_device_form.html', device_form = device_form)

@configure.route('/save_device', methods = ['POST'])
@login_required
def save_device():
    check_configurator()
    id = int(request.form.get('device_id'))
    if id:
        # Existing device
        device = Device.query.get_or_404(id)
        device_form = EditDeviceForm(prefix = 'device_', obj = device)
    else:
        # New device
        device = Device(kind = int(request.form.get('device_kind')))
        device_form = NewDeviceForm(prefix = 'device_', obj = device)
    device_config = device_kinds[device.kind]
    init_device_id_choices(device_form, device_config)
    # Try to validate form first
    if device_form.validate():
        # Temporarily store id to restore it after it is overwritten by populate_obj
        id = device.id
        device_form.populate_obj(device)
        device.id = id
        # If uploaded, read uploaded SVG file (XML)
        db.session.add(device)
        db.session.commit()
        print('save_device() OK')
        return jsonify(
            result = 'OK',
            devices = get_devices(device.config_id))
    else:
        print('save_device() ERROR')
        print(device_form.errors)
        return jsonify(
            result = 'ERROR',
            form = render_template('configure/edit_device_form.html', device_form = device_form))

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

@configure.route('/delete_device/<int:id>', methods = ['POST'])
@login_required
def delete_device(id):
    check_configurator()
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    #TODO send flash throug JSON...
    flash('Module has been deleted', 'success')
    return get_devices(device.config_id)

def init_device_id_choices(device_form, device_config):
    choices = []
    for allowed_id in device_config.allowed_ids:
        choices.append((allowed_id, str(allowed_id)))
    device_form.device_id.choices = choices

def validate_device_form(device_form, device, is_new):
    #TODO optimize models to directly get config from device
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
