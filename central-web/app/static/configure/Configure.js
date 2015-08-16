$(document).ready(function() {
	// ViewModel for configuration dialog (only)
	function EditConfigurationViewModel() {
		var self = this;
		self.name = ko.observable();
		self.lockcode = ko.observable();
		self.map_area_filename = ko.observable();
		self.hasMap = false;
		self.mustDeleteMap = false;
		self.mustUploadMap = false;
		//TODO LATER add devices and alerts thresholds
		self.isNew = ko.observable();
		
		var PROPERTIES = ['name', 'lockcode', 'map_area'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);
		
		self.toJSON = function() {
			return ko.utils.extract(self, PROPERTIES);
		}
		
		// Internal functions
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

		//TODO will need to get additional details through JSON calls
		self.reset = function(newConfig) {
			self.config = newConfig;
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
			$('#config_map_form').get(0).reset();
		}
		
		self.saveConfig = function() {
			ko.utils.ajax(self.uri, 'PUT', self.toJSON()).fail(self.errors.errorHandler).done(function(config) {
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
			ko.utils.ajax('/api/1.0/configurations', 'POST', self.toJSON()).fail(self.errors.errorHandler).done(function(config) {
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
	
//	// AJAX function to prepare and open dialog to edit configuration
//	function openEditConfigDialog()
//	{
//		// Load data for this config
//		var id = $(this).attr('data-config');
//		var url = sprintf('/configure/get_config/%d', id);
//		// Send AJAX request
//		$.ajax({
//			type: 'GET',
//			url: url,
//			success: function(dialog) {
//				// update config dialog info
//				$('#config-dialog').replaceWith(dialog);
//				// check if devices already exist for this configuration
//				updateDevicesList($('.devices-list > tbody').html().trim());
//				$('#config-dialog').modal('show');
//			}
//		});
//		return false;
//	}
//	
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
//	// AJAX function to save configuration
//	function submitConfig()
//	{
//		// Submit form alongside map file if provided
//		fd = new FormData($('#config_form').get(0));
//		$.ajax({
//			url: '/configure/save_config',
//			type: 'POST',
//			data: fd,
//			processData: false,
//			contentType: false,
//			success: function(results) {
//				// Check if form submission is valid
//				if (results.result === 'OK') {
//					// If OK, update config list, flash messages, and hide dialog
//					updateConfigsList(results.configs);
//					$('#flash-messages').html(results.flash);
//					$('#config-dialog').modal('hide');
//					//TODO if new config we should go ahead with edit config!!!
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
//	
//	// AJAX function to get form html to create a new device for current configuration
//	function openCreateDeviceForm()
//	{
//		// Get config id and device kind from clicked link
//		var id = $(this).attr('data-config');
//		var kind = $(this).attr('data-kind');
//		var url = sprintf('/configure/get_new_device_form/%d/%d', id, kind);
//		// Get form through AJAX
//		prepareDeviceForm(url);
//		return true;
//	}
//	
//	// AJAX function to get form html to edit an existing device for current configuration
//	function openEditDeviceForm()
//	{
//		// Get device id from clicked link
//		var id = $(this).attr('data-device');
//		var url = sprintf('/configure/get_edit_device_form/%d', id);
//		// Get form through AJAX
//		prepareDeviceForm(url);
//		return false;
//	}
//	
//	function prepareDeviceForm(url)
//	{
//		// Get form through AJAX
//		$.ajax({
//			type: 'GET',
//			url: url,
//			success: function(form) {
//				// Add form to DOM
//				$('#device_form').replaceWith(form);
//				// Disable all config_form
//				$('#config_name').attr('disabled', true);
//				$('#config_lockcode').attr('disabled', true);
//				$('#config_map_area_file').attr('disabled', true);
//				$('.device-edit').attr('disabled', true);
//				$('.device-delete').attr('disabled', true);
//				$('#create-device').attr('disabled', true);
//				$('#config_submit').attr('disabled', true);
//			}
//		});
//	}
//	
//	function closeDeviceForm()
//	{
//		// Disable all config_form
//		$('#config_name').attr('disabled', false);
//		$('#config_lockcode').attr('disabled', false);
//		$('#config_map_area_file').attr('disabled', false);
//		$('.device-edit').attr('disabled', false);
//		$('.device-delete').attr('disabled', false);
//		$('#create-device').attr('disabled', false);
//		$('#config_submit').attr('disabled', false);
//		$('#device_form').hide();
//	}
//	
//	// AJAX function to save device
//	function submitDevice()
//	{
//		// Submit device form
//		fd = new FormData($('#device_form').get(0));
//		$.ajax({
//			url: '/configure/save_device',
//			type: 'POST',
//			data: fd,
//			processData: false,
//			contentType: false,
//			success: function(results) {
//				// Remove flash messages if any
//				$('#flash-messages').html('');
//				// Check if form submission is valid
//				if (results.result === 'OK') {
//					// If OK, update devices list and hide device form
//					updateDevicesList(results.devices);
//					closeDeviceForm();
//				} else {
//					// Show form errors by replacing the form
//					$('#device_form').replaceWith(results.form);
//				}
//			}
//		});
//		return false;
//	}
//	
//	// AJAX function to cancel device edit form
//	function cancelDevice()
//	{
//		closeDeviceForm();
//		return false;
//	}
//	
//	// AJAX function to delete a configuration
//	function deleteDevice()
//	{
//		if (window.confirm('Are you sure you want to remove this module?')) {
//			var id = $(this).attr('data-device');
//			var url = sprintf('/configure/delete_device/%d', id);
//			// Send AJAX request
//			$.ajax({
//				type: 'POST',
//				url: url,
//				success: function(results) {
//					$('#flash-messages').html(results.flash);
//					updateDevicesList(results.devices);
//				}
//			});
//		}
//		return false;
//	}
//	
//	function updateDevicesList(devices)
//	{
//		if (devices.length == 0) {
//			$('.devices-list').hide();
//			$('#empty-devices-list').show();
//		} else {
//			$('#empty-devices-list').hide();
//			$('.devices-list > tbody').html(devices);
//			// Finally show the configurations list
//			$('.devices-list').show();
//		}
//	}
//	
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
//	
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
//	function collapseConfigDetail()
//	{
//		// Find all already collapsed elements and uncollapse them
//		$('.collapse.in').collapse('hide');
//	}
	
	// Now get the list of configurations through AJAX
//	$.ajax({
//		type: 'GET',
//		url: '/configure/get_configs_list',
//		success: updateConfigsList
//	});
	
	// Register event handlers
	// - for list of configurations
//	$('.config-new').on('click', openNewConfigDialog);
//	$('.configs-list').on('click', '.config-set-current:not(.disabled)', setCurrentConfig);
//	$('.configs-list').on('click', '.config-delete', deleteConfig);
//	$('.configs-list').on('click', '.config-edit', openEditConfigDialog);
//	$('.configs-list').on('click', '.config-map', openConfigMapDialog);
	// - for config modal dialog
//	$('#modal-content').on('click', '.cancel', function() {
//		$('#config-dialog').modal('hide');
//	});
//	$('#modal-content').on('submit', '#config_form', submitConfig);
//	$('#modal-content').on('show.bs.collapse', collapseConfigDetail);
//	// - for config map (devices location setup)
//	$('#modal-content').on('submit', '#config_map_form', submitMap);
//	// - for list of modules
//	$('#modal-content').on('click', '.create-device', openCreateDeviceForm);
//	$('#modal-content').on('click', '.device-edit', openEditDeviceForm);
//	$('#modal-content').on('click', '.device-delete', deleteDevice);
	// - for device form
//	$('#modal-content').on('click', '.device-submit', submitDevice);
//	$('#modal-content').on('click', '.device-cancel', cancelDevice);
//	// - for ping alerts settings
//	$('#modal-content').on('click', '#config_ping_alerts button', addPingAlert);
//	$('#modal-content').on('click', '.ping-alert-remove', removePingAlert);
//	// - for ping alerts settings
//	$('#modal-content').on('click', '#config_voltage_alerts button', addVoltageAlert);
//	$('#modal-content').on('click', '.voltage-alert-remove', removeVoltageAlert);
});
