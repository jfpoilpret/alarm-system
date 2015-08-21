$(document).ready(function() {
	// ViewModel for device form (only)
	// NOTE: devices changes are immediately transferred to server (not when saving whole config)
	function EditDeviceModel() {
		var self = this;
		self.name = ko.observable();
		self.voltage_threshold = ko.observable();
		self.device_id = ko.observable();
		
		self.showDeviceForm = ko.observable(false);
		self.allDeviceIDs = ko.observableArray();

		self.isNew = ko.observable();

		var PROPERTIES = ['name', 'voltage_threshold', 'device_id', 'kind'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);

		// Internal functions
		var toJSON = function() {
			return ko.utils.extract(self, PROPERTIES);
		}
		var postDevice = function(done) {
			var uri = '/api/1.0/configurations/' + self.config_id + '/devices';
			ko.utils.ajax(uri, 'POST', toJSON()).fail(self.errors.errorHandler).done(done);
		}
		var putDevice = function(done) {
			ko.utils.ajax(self.uri, 'PUT', toJSON()).fail(self.errors.errorHandler).done(done);
		}
		var showForm = function(show) {
			$('.disablable').attr('disabled', show);
			self.showDeviceForm(show);
		}
		
		self.cancelDeviceForm = function() {
			showForm(false);
		}
		
		self.saveDevice = function() {
			if (self.isNew()) {
				postDevice(function(device) {
					editConfigViewModel.addDevice(device);
					showForm(false);
				});
			} else {
				putDevice(function(device) {
					editConfigViewModel.updateDevice(self.id, device);
					showForm(false);
				});
			}
		}
		
		self.reset = function(configId, deviceCreator, newDevice) {
			var isNew = (newDevice === undefined);
			if (isNew) {
				newDevice = {
					id: undefined,
					uri: undefined,
					name: undefined,
					kind: (deviceCreator ? deviceCreator.kind : undefined),
					voltage_threshold: undefined,
					device_id: undefined
				};
			}
			self.id = newDevice.id;
			self.config_id = configId;
			self.uri = newDevice.uri;
			self.kind = newDevice.kind;
			self.name(newDevice.name);
			self.voltage_threshold(newDevice.voltage_threshold);
			self.allDeviceIDs(deviceCreator ? deviceCreator.deviceIds : []);
			self.device_id(newDevice.device_id);
			self.isNew(isNew);
			self.errors.clear();
			if (isNew) {
				//TODO
			}
			if (deviceCreator)
				showForm(true);
		}
		
		self.reset();
	}
	
	// ViewModel for configuration dialog (only)
	function EditConfigurationViewModel() {
		var self = this;
		self.name = ko.observable();
		self.lockcode = ko.observable();
		self.map_area_filename = ko.observable();
		self.hasMap = false;
		self.mustDeleteMap = false;
		self.mustUploadMap = false;
		
		self.devices = ko.observableArray();
		self.emptyList = ko.pureComputed(function() {
			return self.devices().length == 0;
		});
		self.editDeviceModel = new EditDeviceModel();
		
		//TODO LATER add alerts thresholds
		self.isNew = ko.observable();
		
		var PROPERTIES = ['name', 'lockcode', 'map_area'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);

		// List of modules kind that can be created through dropdown button
		self.deviceCreators = [
   			{label: 'Add Keypad Module',			kind: 'Keypad', deviceIds: ko.utils.range(0x10, 0x14)},
			{label: 'Add Motion Detection Module',	kind: 'Motion', deviceIds: ko.utils.range(0x20, 0x30)},
			{label: 'Add Camera Module',			kind: 'Camera', deviceIds: ko.utils.range(0x30, 0x38)}
		];
		
		// Internal functions
		var compare = ko.utils.compareByNumber('device_id');
		var findCreator = function(kind) {
			var found = $.grep(self.deviceCreators, function(creator) {
				return creator.kind == kind;
			});
			return found ? found[0] : null;
		}
		var toJSON = function() {
			return ko.utils.extract(self, PROPERTIES);
		}
		var postMap = function(uri, done) {
			// Submit form alongside map file if provided
			var fd = new FormData($('#config_map_form').get(0));
			$.ajax({
				url: uri,
				type: 'POST',
				data: fd,
				processData: false,
				contentType: false
			}).fail(self.errors.errorHandler).done(done);
		}
		var deleteMap = function(uri, done) {
			// Submit form alongside map file if provided
			$.ajax({
				url: uri,
				type: 'DELETE'
			}).fail(self.errors.errorHandler).done(done);
		}

		self.reset = function(newConfig) {
			var isNew = (newConfig === undefined);
			if (isNew) {
				newConfig = {
					id: undefined,
					uri: undefined,
					name: undefined,
					lockcode: undefined,
					map_area_filename: undefined
				};
			}
			self.id = newConfig.id;
			self.uri = newConfig.uri;
			self.name(newConfig.name);
			self.lockcode(newConfig.lockcode);
			self.map_area_filename(newConfig.map_area_filename);
			self.hasMap = newConfig.map_area_filename ? true : false;
			self.mustDeleteMap = false;
			self.mustUploadMap = false;
			self.isNew(isNew);
			self.errors.clear();
			if (isNew) {
				// Clear devices list
				self.devices([]);
			} else {
				// Read devices from server
				$.getJSON(newConfig.devices, self.devices);
				self.devices.sort(compare);
				//TODO will need to get additional details through JSON calls
			}
			$('#config_map_form').get(0).reset();
		}
		
		//TODO refactor 2 next functions in one common code!
		self.saveConfig = function() {
			ko.utils.ajax(self.uri, 'PUT', toJSON()).fail(self.errors.errorHandler).done(function(config) {
				// Signal VM of all configs
				configurationsViewModel.configUpdated(config);
				var done = function(config) {
					configurationsViewModel.configUpdated(config);
					// Add message
					flashMessages.clear();
					flashMessages.success('Configuration \'' + config.name + '\' has been saved');
					// Hide dialog
					$('#config-dialog').modal('hide');
				}
				// Check if we need to upload or delete a map file
				if (self.mustUploadMap) {
					postMap(config.map, done);
				} else if (self.mustDeleteMap) {
					deleteMap(config.map, done);
				} else {
					done(config);
				}
			});
		}
		
		self.saveNewConfig = function() {
			ko.utils.ajax('/api/1.0/configurations', 'POST', toJSON()).fail(self.errors.errorHandler).done(function(config) {
				// Signal VM of all configs
				configurationsViewModel.configAdded(config);
				var done = function(config) {
					configurationsViewModel.configUpdated(config);
					// Add message
					flashMessages.clear();
					flashMessages.success('New configuration \'' + config.name + '\' has been created');
					// Hide dialog
					$('#config-dialog').modal('hide');
				}
				// Check if we need to upload a map file
				if (self.mustUploadMap) {
					postMap(config.map, done);
				} else if (self.mustDeleteMap) {
					deleteMap(config.map, done);
				} else {
					done(config);
				}
			});
		}
		
		self.showMapUpload = function(config) {
			// Simulate click on hidden input file
			$('#map_area').click();
		}
		
		self.deleteMap = function(config) {
			// Confirm then remove from VM only
			if (window.confirm('Are you sure you want to delete the configured map file?')) {
				self.mustDeleteMap = self.hasMap;
				self.map_area_filename('');
				$('#config_map_form').get(0).reset();
			}
		}
		
		self.mapUploadChanged = function(config, event) {
			self.map_area_filename($('#map_area').get(0).files[0].name);
			self.mustDeleteMap = false;
			self.mustUploadMap = true;
		}
		
		self.editNewDevice = function(creator) {
			self.editDeviceModel.reset(self.id, creator);
		}
		
		self.editDevice = function(device) {
			var creator = findCreator(device.kind);
			self.editDeviceModel.reset(self.id, creator, device);
		}
		
		self.addDevice = function(device) {
			self.devices.push(device);
			self.devices.sort(compare);
		}
		
		self.updateDevice = function(id, device) {
			// Replace existing device and TODO re-sort list
			index = ko.utils.firstIndex(self.devices.peek(), ko.utils.filterById(device.id));
			self.devices.peek()[index] = device;
			self.devices.sort(compare);
		}
		
		// Initialize the VM the first time
		self.reset();
	}
	
	// ViewModel for list of configurations
	function ConfigurationsViewModel(configs) {
		var self = this;
		
		// Local utility functions (internal use)
		var initConfig = function(config) {
			return config;
		}
		var compare = ko.utils.compareByString('name');
		
		// Add additional properties/methods to each config
		self.configurations = ko.observableArray($.map(configs, initConfig).sort(compare));
		self.emptyList = ko.pureComputed(function() {
			return self.configurations().length == 0;
		});
		
		self.deleteConfig = function(config) {
			if (window.confirm('Are you sure you want to remove this configuration?')) {
				ko.utils.ajax(config.uri, 'DELETE').done(function(results) {
					self.configurations.remove(ko.utils.filterById(config.id));
					// Add message
					flashMessages.clear();
					flashMessages.success('Configuration \'' + config.name + '\' has been removed');
				});
			}
		}
		
		self.setCurrent = function(config) {
			//TODO maybe create special uri for current config first?
			console.log('setCurrent');
			console.log(config);
		}
		
		self.editConfig = function(config) {
			// Reset Configuration ViewModel and show dialog
			editConfigViewModel.reset(config);
			$('#config-dialog').modal('show');
		}

		self.editConfigMap = function(config) {
			console.log('editConfigMap');
			console.log(config);
		}

		self.editNewConfig = function() {
			// Reset Configuration ViewModel and show dialog
			editConfigViewModel.reset();
			$('#config-dialog').modal('show');
		}

		self.configUpdated = function(config) {
			// Replace existing config and re-sort list
			index = ko.utils.firstIndex(self.configurations.peek(), ko.utils.filterById(config.id));
			self.configurations.peek()[index] = initConfig(config);
			self.configurations.sort(compare);
		}
		
		self.configAdded = function(config) {
			// Add new config and re-sort list
			self.configurations.push(initConfig(config));
			self.configurations.sort(compare);
		}
	}
	
	// Declare all VM
	var flashMessages = ko.utils.getFlashMessages($('#flash-messages').get(0));
	var editConfigViewModel = new EditConfigurationViewModel();
	ko.applyBindings(editConfigViewModel, $('#config-dialog').get(0));
	var configurationsViewModel;

	// Now get the list of configurations through AJAX and populate the global VM
	$.getJSON('/api/1.0/configurations', function(configs) {
		configurationsViewModel = new ConfigurationsViewModel(configs);
		ko.applyBindings(configurationsViewModel, $('.configurations').get(0));
	});
	
//	function openConfigMapDialog()
//	{
//		// Load data for this config
//		var id = $(this).attr('data-config');
//		var url = sprintf('/configure/get_config_map/%d', id);
//		// Send AJAX request
//		$.ajax({
//			type: 'GET',
//			url: url,
//			success: function(dialog) {
//				// update config dialog info
//				$('#config-dialog').replaceWith(dialog);
//				$('#config-dialog').modal('show');
//			    $('[data-toggle="popover"]').popover(
//			    	{'container': 'body', 'trigger': 'hover focus', 'placement': 'right'});
//			}
//		});
//		return false;
//	}
//	
//	// AJAX function to save map configuration
//	function submitMap()
//	{
//		// Submit form alongside map file if provided
//		fd = new FormData($('#config_map_form').get(0));
//		$.ajax({
//			url: '/configure/save_config_map',
//			type: 'POST',
//			data: fd,
//			processData: false,
//			contentType: false,
//			success: function(results) {
//				if (results.result === 'OK') {
//					$('#flash-messages').html(results.flash);
//					$('#config-dialog').modal('hide');
//				} else {
//					// Remove flash messages if any
//					$('#flash-messages').html('');
//					// Hide dialog before replacing content (otherwise background may stay forever)
//					$('#config-dialog').modal('hide');
//					// Show form errors by replacing the form
//					$('#config-dialog').replaceWith(results.form);
//					// Have to show dialog again as replacement hid it
//					$('#config-dialog').modal('show');
//				}
//			}
//		});
//		return false;
//	}

//	// AJAX function to add a new ping alert setting
//	function addPingAlert()
//	{
//		var id = $(this).attr('data-config');
//		var level = $(this).attr('data-level');
//		var time = $(this).closest('div.input-group').children('input.ping-alert-time').val();
//		// Prepare JSON
//		var request = {
//			id: id,
//			level: level,
//			time: time
//		};
//		// Send AJAX request
//		$.ajax({
//			type: 'POST',
//			url: '/configure/add_ping_alert',
//			data: JSON.stringify(request),
//			contentType: 'application/json',
//			processData: false,
//			success: function(results) {
//				$('#flash-messages').html('');
//				$('#config_ping_alerts .list-group').html(results);
//			}
//		});
//		return false;
//	}

//	// AJAX function to delete a ping alert setting
//	function removePingAlert()
//	{
//		var id = $(this).attr('data-alert');
//		var url = sprintf('/configure/delete_ping_alert/%d', id);
//		// Send AJAX request
//		$.ajax({
//			type: 'POST',
//			url: url,
//			success: function(results) {
//				$('#flash-messages').html('');
//				$('#config_ping_alerts .list-group').html(results);
//			}
//		});
//		return false;
//	}
//	
//	// AJAX function to add a new voltage alert setting
//	function addVoltageAlert()
//	{
//		var id = $(this).attr('data-config');
//		var level = $(this).attr('data-level');
//		var $parent = $(this).closest('li.list-group-item');
//		var rate = $parent.find('input.voltage-alert-threshold').val();
//		var time = $parent.find('input.voltage-alert-time').val();
//		// Prepare JSON
//		var request = {
//			id: id,
//			level: level,
//			rate: rate,
//			time: time
//		};
//		// Send AJAX request
//		$.ajax({
//			type: 'POST',
//			url: '/configure/add_voltage_alert',
//			data: JSON.stringify(request),
//			contentType: 'application/json',
//			processData: false,
//			success: function(results) {
//				$('#flash-messages').html('');
//				$('#config_voltage_alerts .list-group').html(results);
//			}
//		});
//		return false;
//	}
//	
//	// AJAX function to delete a ping voltage setting
//	function removeVoltageAlert()
//	{
//		var id = $(this).attr('data-alert');
//		var url = sprintf('/configure/delete_voltage_alert/%d', id);
//		// Send AJAX request
//		$.ajax({
//			type: 'POST',
//			url: url,
//			success: function(results) {
//				$('#flash-messages').html('');
//				$('#config_voltage_alerts .list-group').html(results);
//			}
//		});
//		return false;
//	}
	
	// This handler is called when a detail part of the config dialog is collapsed
	// so that it uncollapses other parts (only one at a time)
	// Note that Bootstrap has offers this behavior already but only inside panels.
	function collapseConfigDetail() {
		// Find all already collapsed elements and uncollapse them
		$('.collapse.in').collapse('hide');
	}
	
	// Register event handlers
	$('#modal-content').on('show.bs.collapse', collapseConfigDetail);
	
//	// - for config map (devices location setup)
//	$('#modal-content').on('submit', '#config_map_form', submitMap);
//	// - for ping alerts settings
//	$('#modal-content').on('click', '#config_ping_alerts button', addPingAlert);
//	$('#modal-content').on('click', '.ping-alert-remove', removePingAlert);
//	// - for ping alerts settings
//	$('#modal-content').on('click', '#config_voltage_alerts button', addVoltageAlert);
//	$('#modal-content').on('click', '.voltage-alert-remove', removeVoltageAlert);
});
