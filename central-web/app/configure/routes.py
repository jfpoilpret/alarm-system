from json import loads
from re import compile
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import update

from app import db
from app.models import Configuration, Device, NoPingTimeAlertThreshold,\
    VoltageRateAlertThreshold
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
    all_configs = Configuration.query.order_by(Configuration.name).all()
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
    id = int(request.form.get('config_id'))
    if id:
        # Existing configuration
        config = Configuration.query.get_or_404(id)
        config_form = EditConfigForm(prefix = 'config_', obj = config)
        device_form = NewDeviceForm(prefix = 'device_')
        success = 'Configuration ''%s'' has been saved'
    else:
        # New configuration
        config = Configuration()
        config_form = NewConfigForm(prefix = 'config_', obj = config)
        device_form = None
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
            form = render_template('configure/dialog_edit_config.html', 
                config = config, config_form = config_form, device_form = device_form))

DEVICEID_REGEX = compile('[0-9]+')
def find_device(config, device_id):
    id = int(DEVICEID_REGEX.findall(device_id)[0])
    return config.devices[id]

@configure.route('/get_config_map/<int:id>')
@login_required
def get_config_map(id):
    check_configurator()
    config = Configuration.query.get_or_404(id)
    if not config.map_area:
        #FIXME use pure AJAX!
        flash('Configuration ''%s'' has no Monitored Zone Map set yet!' % config.name, 'warning')
        return redirect(url_for('.home'))
    config_map_form = DevicesLocationForm(prefix = 'config_', id = id)
    return render_template('configure/dialog_config_map.html', 
        config = config,
        svg_map = prepare_map_for_config(config),
        config_map_form = config_map_form)

@configure.route('/save_config_map', methods = ['POST'])
@login_required
def save_config_map():
    check_configurator()
    config_map_form = DevicesLocationForm(prefix = 'config_')
    if config_map_form.validate():
        config = Configuration.query.get_or_404(config_map_form.id.data)
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
        message  = 'New devices locations for ''%s''  have been saved' % config.name
        return jsonify(result = 'OK', 
            flash = render_template('flash_messages.html', message = message, category = 'success'))
    else:
        return jsonify(result = 'ERROR', form = render_template('configure/dialog_config_map.html', 
            config = config,
            svg_map = prepare_map_for_config(config),
            config_map_form = config_map_form))

@configure.route('/delete_config/<int:id>', methods = ['POST'])
@login_required
def delete_config(id):
    check_configurator()
    config = Configuration.query.get_or_404(id)
    db.session.delete(config)
    db.session.commit()
    message = 'Configuration ''%s'' has been deleted' % config.name
    return jsonify(
        result = 'OK',
        flash = render_template('flash_messages.html', message = message, category = 'success'),
        configs = get_configs_list())

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

@configure.route('/delete_device/<int:id>', methods = ['POST'])
@login_required
def delete_device(id):
    check_configurator()
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    message = 'Module ''%s'' has been deleted' % device.name
    flash('Module has been deleted', 'success')
    return jsonify(
        result = 'OK',
        devices = get_devices(device.config_id),
        flash = render_template('flash_messages.html', message = message, category = 'success'))

def init_device_id_choices(device_form, device_config):
    choices = []
    for allowed_id in device_config.allowed_ids:
        choices.append((allowed_id, str(allowed_id)))
    device_form.device_id.choices = choices

@configure.route('/get_ping_alerts/<int:id>', methods = ['GET'])
@login_required
def get_ping_alerts(id):
    config = Configuration.query.get_or_404(id)
    return render_template('configure/all_ping_alert_rows.html', config = config)

@configure.route('/add_ping_alert', methods = ['POST'])
@login_required
def add_ping_alert():
    check_configurator()
    json = request.get_json()
    ping_alert = NoPingTimeAlertThreshold(
        config_id = json['id'],
        alert_level = json['level'],
        alert_time = json['time'])
    db.session.add(ping_alert)
    db.session.commit()
    # return new list of alerts
    return get_ping_alerts(json['id'])

@configure.route('/delete_ping_alert/<int:id>', methods = ['POST'])
@login_required
def delete_ping_alert(id):
    check_configurator()
    ping_alert = NoPingTimeAlertThreshold.query.get_or_404(id)
    config_id = ping_alert.config_id
    db.session.delete(ping_alert)
    db.session.commit()
    # return new list of alerts
    return get_ping_alerts(config_id)

@configure.route('/get_voltage_alerts/<int:id>', methods = ['GET'])
@login_required
def get_voltage_alerts(id):
    config = Configuration.query.get_or_404(id)
    return render_template('configure/all_voltage_alert_rows.html', config = config)

@configure.route('/add_voltage_alert', methods = ['POST'])
@login_required
def add_voltage_alert():
    check_configurator()
    json = request.get_json()
    voltage_alert = VoltageRateAlertThreshold(
        config_id = json['id'],
        alert_level = json['level'],
        voltage_rate = json['rate'],
        alert_time = json['time'])
    db.session.add(voltage_alert)
    db.session.commit()
    # return new list of alerts
    return get_voltage_alerts(json['id'])

@configure.route('/delete_voltage_alert/<int:id>', methods = ['POST'])
@login_required
def delete_voltage_alert(id):
    check_configurator()
    voltage_alert = VoltageRateAlertThreshold.query.get_or_404(id)
    config_id = voltage_alert.config_id
    db.session.delete(voltage_alert)
    db.session.commit()
    # return new list of alerts
    return get_voltage_alerts(config_id)

