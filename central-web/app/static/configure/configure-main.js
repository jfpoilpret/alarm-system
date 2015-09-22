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
		self.dirtyFlag = new ko.utils.DirtyFlag([self.name, self.voltage_threshold, self.device_id]);

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
			//FIXME when show == true, this enables all components, even those that should not be
			// (e.g. save button that have data-bind enable)
			$('.disablable').attr('disabled', show);
			self.showDeviceForm(show);
			if (show)
				$('#device_name').focus();
		}
		
		self.cancelDeviceForm = function() {
			showForm(false);
		}
		
		self.saveDevice = function() {
			if (self.isNew()) {
				postDevice(function(device) {
					globalViewModel.config().configEditor.addDevice(device);
					showForm(false);
				});
			} else {
				putDevice(function(device) {
					globalViewModel.config().configEditor.updateDevice(self.id, device);
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
			self.dirtyFlag.reset();
			if (deviceCreator)
				showForm(true);
		}
		
		self.reset();
	}
	
	function AlertThresholdsModel(level, label, css, icon, hasVoltage) {
		var self = this;
		self.level = level;
		self.itemCss = 'list-group-item-' + css;
		self.levelIcon = 'glyphicon-' + icon;
		self.levelLabel = label;
		self.thresholds = ko.observableArray();
		self.newTime = ko.observable();
		self.newVoltage = ko.observable();
		self.dirty = false;

		var compareTime = function(t1, t2) {
			return t2 - t1;
		}
		var compareVoltage = function(t1, t2) {
			if (t1.voltage === t2.voltage)
				return t2.time - t1.time;
			return t1.voltage - t2.voltage;
		}
		var compare = hasVoltage ? compareVoltage : compareTime;
		
		self.setThresholds = function(thresholds) {
			self.dirty = false;
			self.thresholds(thresholds);
			self.thresholds.sort(compare);
		}
		self.removeThreshold = function(threshold) {
			self.dirty = true;
			self.thresholds.remove(threshold);
		}
		self.addTimeThreshold = function() {
			var time = self.newTime();
			if ($.isNumeric(time)) {
				time = Number(time);
				if (self.thresholds.indexOf(time) < 0) {
					self.dirty = true;
					self.thresholds.push(time);
					self.thresholds.sort(compare);
				}
				self.newTime(undefined);
			}
		}
		self.addVoltageThreshold = function() {
			var voltage = self.newVoltage();
			var time = self.newTime();
			if ($.isNumeric(time) && $.isNumeric(voltage)) {
				var threshold = {rate: Number(voltage), time: Number(time)};
				if (self.thresholds.indexOf(threshold) < 0) {
					self.dirty = true;
					self.thresholds.push(threshold);
					self.thresholds.sort(compare);
				}
				self.newTime(undefined);
				self.newVoltage(undefined);
			}
		}
	}
	
	// ViewModel for configuration dialog (only)
	function EditConfigurationViewModel() {
		var self = this;
		// Configurations entity fields
		self.name = ko.observable();
		self.lockcode = ko.observable();
		self.map_area_filename = ko.observable();
		self.hasMap = false;
		self.mustDeleteMap = false;
		self.mustUploadMap = false;
		self.isNew = ko.observable();

		// Devices
		self.devices = ko.observableArray();
		self.emptyDevicesList = ko.pureComputed(function() {
			return self.devices().length == 0;
		});
		self.editDeviceModel = new EditDeviceModel();
		
		// Thresholds for no ping alerts
		self.noPingThresholds = [
            new AlertThresholdsModel('info', 'Info', 'info', 'info-sign'),
            new AlertThresholdsModel('warning', 'Warning', 'warning', 'exclamation-sign'),
            new AlertThresholdsModel('alarm', 'Alarm', 'danger', 'warning-sign')
		];
		// Thresholds for voltage rate alerts
		self.voltageThresholds = [
             new AlertThresholdsModel('info', 'Info', 'info', 'info-sign', true),
             new AlertThresholdsModel('warning', 'Warning', 'warning', 'exclamation-sign', true),
             new AlertThresholdsModel('alarm', 'Alarm', 'danger', 'warning-sign', true)
 		];

		// Errors
		var PROPERTIES = ['name', 'lockcode', 'map_area'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);
		
		// Dirty flag
		var dirtyObservables = [self.name, self.lockcode, self.map_area_filename];
		$.each(self.noPingThresholds, function(index, value) { dirtyObservables.push(value.thresholds); });
		$.each(self.voltageThresholds, function(index, value) { dirtyObservables.push(value.thresholds); });
		self.dirtyFlag = new ko.utils.DirtyFlag(dirtyObservables);

		// List of modules kind that can be created through dropdown button
		self.deviceCreators = [
   			{label: 'Add Keypad Module',			kind: 'Keypad', deviceIds: ko.utils.range(0x10, 0x14)},
			{label: 'Add Motion Detection Module',	kind: 'Motion', deviceIds: ko.utils.range(0x20, 0x30)},
			{label: 'Add Camera Module',			kind: 'Camera', deviceIds: ko.utils.range(0x30, 0x38)}
		];
		
		// Internal functions
		var compare = ko.utils.compareByNumber('device_id');
		var findNoPingThreshold = function(level) {
			var found = $.grep(self.noPingThresholds, function(threshold) {
				return threshold.level === level;
			});
			return found ? found[0] : null;
		}
		var findVoltageThreshold = function(level) {
			var found = $.grep(self.voltageThresholds, function(threshold) {
				return threshold.level === level;
			});
			return found ? found[0] : null;
		}
		var findCreator = function(kind) {
			var found = $.grep(self.deviceCreators, function(creator) {
				return creator.kind === kind;
			});
			return found ? found[0] : null;
		}
		var toJSON = function() {
			return ko.utils.extract(self, PROPERTIES);
		}
		var postMap = function(config) {
			// Submit form alongside map file if provided
			return $.ajax({
				url: config.map,
				type: 'POST',
				data: new FormData($('#config_map_form').get(0)),
				processData: false,
				contentType: false
			}).fail(self.errors.errorHandler);
		}
		var deleteMap = function(config) {
			return ko.utils.ajax(config.map, 'DELETE').fail(self.errors.errorHandler);
		}
		var putThresholds = function(array, uri) {
			var thresholds = {};
			$.each(array, function(index, threshold) {
				thresholds[threshold.level] = threshold.thresholds();
			});
			return ko.utils.ajax(uri, 'PUT', thresholds).fail(self.errors.errorHandler);
		}
		var putNoPingThresholds = function() {
			return putThresholds(self.noPingThresholds, self.uriNoPingThresholds);
		}
		var putVoltageThresholds = function() {
			return putThresholds(self.voltageThresholds, self.uriVoltageThresholds);
		}

		self.reset = function(newConfig) {
			var isNew = (newConfig === undefined);
			if (isNew) {
				newConfig = {
					id: undefined,
					uri: undefined,
					name: undefined,
					lockcode: undefined,
					map_area_filename: null,
					no_ping_thresholds: undefined,
					voltage_thresholds: undefined
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
			self.uriNoPingThresholds = newConfig.no_ping_thresholds;
			self.uriVoltageThresholds = newConfig.voltage_thresholds;
			self.isNew(isNew);
			self.errors.clear();
			if (isNew) {
				// Clear devices list
				self.devices([]);
				$.each(self.noPingThresholds, function(index, thresholds) {
					thresholds.setThresholds([]);
				});
				$.each(self.voltageThresholds, function(index, thresholds) {
					thresholds.setThresholds([]);
				});
				self.dirtyFlag.reset();
			} else {
				// Read devices from server
				$.getJSON(newConfig.devices, function(devices) {
					self.devices(devices);
					self.devices.sort(compare);
				});
				// Read no ping alert thresholds from server
				$.getJSON(newConfig.no_ping_thresholds, function(thresholds) {
					$.each(thresholds, function(level, times) {
						var threshold = findNoPingThreshold(level);
						threshold.setThresholds(times);
					});
					self.dirtyFlag.reset();
				});
				// Read voltage alert thresholds from server
				$.getJSON(newConfig.voltage_thresholds, function(thresholds) {
					$.each(thresholds, function(level, times) {
						var threshold = findVoltageThreshold(level);
						threshold.setThresholds(times);
					});
					self.dirtyFlag.reset();
				});
			}
			if ($('#config_map_form').length)
				$('#config_map_form').get(0).reset();
		}
		
		self.saveConfig = function() {
			var chain = ko.utils.ajax(self.uri, 'PUT', toJSON()).
				fail(self.errors.errorHandler).
				done(globalViewModel.config().configUpdated);
			if (self.mustUploadMap) {
				chain = chain.then(postMap).done(globalViewModel.config().configUpdated);
			} else if (self.mustDeleteMap) {
				chain = chain.then(deleteMap).done(globalViewModel.config().configUpdated);
			}
			// Add necessary PUT for no ping thresholds alerts
			if ($.grep(self.noPingThresholds, function(item) { return item.dirty; }).length !== 0) {
				chain = chain.then(putNoPingThresholds);
			}
			// Add necessary PUT for no ping thresholds alerts
			if ($.grep(self.voltageThresholds, function(item) { return item.dirty; }).length !== 0) {
				chain = chain.then(putVoltageThresholds);
			}
			chain.done(function() {
				// Add message
				globalViewModel.flashMessages.clear();
//				globalViewModel.flashMessages.success('Configuration \'' + config.name + '\' has been saved');
				globalViewModel.flashMessages.success('Configuration has been saved');
				// Hide dialog
				$('#config-dialog').modal('hide');
			});
		}
		
		self.saveNewConfig = function() {
			var chain = ko.utils.ajax('/api/1.0/configurations', 'POST', toJSON()).
				fail(self.errors.errorHandler).
				done(globalViewModel.config().configAdded);
			if (self.mustUploadMap) {
				chain = chain.then(postMap).done(globalViewModel.config().configUpdated);
			}
			chain.done(function(config) {
				// Add message
				globalViewModel.flashMessages.clear();
				globalViewModel.flashMessages.success('New configuration \'' + config.name + '\' has been created');
				// Hide dialog
				$('#config-dialog').modal('hide');
				// Open Edit Config dialog
				globalViewModel.config().editConfig(config);
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
				self.map_area_filename(null);
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
		
		self.deleteDevice = function(device) {
			if (window.confirm('Are you sure you want to remove this module?')) {
				ko.utils.ajax(device.uri, 'DELETE').done(function(results) {
					self.devices.remove(ko.utils.filterById(device.id));
					// Add message
					globalViewModel.flashMessages.clear();
					globalViewModel.flashMessages.success('Module \'' + device.name + '\' has been removed');
				});
			}
		}
		
		self.addDevice = function(device) {
			self.devices.push(device);
			self.devices.sort(compare);
		}
		
		self.updateDevice = function(id, device) {
			// Replace existing device and re-sort list
			index = ko.utils.firstIndex(self.devices.peek(), ko.utils.filterById(device.id));
			self.devices.peek()[index] = device;
			self.devices.sort(compare);
		}
		
		// Initialize the VM the first time
		self.reset();
	}
	
	function EditMapLocationsViewModel() {
		var self = this;
		self.name = ko.observable();
		self.svgMap = ko.observable();
		self.errors = new ko.errors.ErrorsViewModel();
		
		self.reset = function(name, uri) {
			DeviceCoordinates = {};
			self.uri = uri;
			self.name(name);
			self.errors.clear();
			if (uri) {
				// Read SVG ready for drag&drop from server
				$.getJSON(uri + '?prepare_for=configuration', function(map) {
					self.svgMap(map);
				    $('[data-toggle="popover"]').popover(
				    	{'container': 'body', 'trigger': 'hover focus', 'placement': 'right'});
				});
			}
		}
		
		self.saveMapConfig = function() {
			// Save new devices locations
			var promise = null;
			$.each(DeviceCoordinates, function(uri, location) {
				var next = ko.utils.ajax(uri, 'PUT', {location_x: location.x, location_y: location.y});
				promise = (promise ? promise.then(next) : next);
			});
			promise.fail(self.errors.errorHandler).done(function() {
				$('#config-map-dialog').modal('hide');
				// Add message
				globalViewModel.flashMessages.clear();
				globalViewModel.flashMessages.success('Devices locations for configuration \'' + self.name() + '\' have been saved');
			});
		}
		
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
		
		self.configEditor = new EditConfigurationViewModel();
		self.configMapEditor = new EditMapLocationsViewModel();
		
		self.deleteConfig = function(config) {
			if (window.confirm('Are you sure you want to remove this configuration?')) {
				ko.utils.ajax(config.uri, 'DELETE').done(function(results) {
					self.configurations.remove(ko.utils.filterById(config.id));
					// Add message
					globalViewModel.flashMessages.clear();
					globalViewModel.flashMessages.success('Configuration \'' + config.name + '\' has been removed');
				});
			}
		}
		
		self.setCurrent = function(config) {
			ko.utils.ajax('/api/1.0/configurations/current?id=' + config.id, 'POST').done(function() {
				// Update all configurations
				var configs = self.configurations();
				$.each(configs, function(index, conf) {
					conf.current = (conf.id === config.id);
				});
				// Force configurations list refresh
				self.configurations([]);
				self.configurations(configs);
			});
		}
		
		self.editConfig = function(config) {
			// Reset Configuration ViewModel and show dialog
			self.configEditor.reset(config);
			$('#config-dialog').modal('show');
			$('#config_name').focus();
		}

		self.editConfigMap = function(config) {
			// Reset Map Locations ViewModel and show dialog
			self.configMapEditor.reset(config.name, config.map);
			$('#config-map-dialog').modal('show');
		}

		self.editNewConfig = function() {
			// Reset Configuration ViewModel and show dialog
			self.configEditor.reset();
			$('#config-dialog').modal('show');
			$('#config_name').focus();
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

	// Create main VM (and children hierarchy) for configuration
	$.getJSON('/api/1.0/configurations', function(configs) {
		globalViewModel.config(new ConfigurationsViewModel(configs));
	});
	
	// This handler is called when a detail part of the config dialog is collapsed
	// so that it uncollapses other parts (only one at a time)
	// Note that Bootstrap has offers this behavior already but only inside panels.
	function collapseConfigDetail() {
		// Find all already collapsed elements and uncollapse them
		$('.collapse.in').collapse('hide');
	}
	
	// Register event handlers
	$('#modal-content').on('show.bs.collapse', collapseConfigDetail);
});
