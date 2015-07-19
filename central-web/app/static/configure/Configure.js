$(document).ready(function() {
	// Store empty content of form as a way to reset it
	var $newConfigForm = $('#config-dialog').clone();

	// Function to show dialof for creating new configuration
	function openNewConfigDialog()
	{
		// Restore form to initial content
		$('#config-dialog').replaceWith($newConfigForm.clone());
		$('#config-dialog').modal('show');
	}

	// AJAX function to prepare and open dialog to edit configuration
	function openEditConfigDialog()
	{
		// Load data for this config
		var id = $(this).attr('data-config');
		var url = sprintf('/configure/get_config/%d', id);
		// Send AJAX request
		$.ajax({
			type: 'GET',
			url: url,
			success: function(dialog) {
				// update config dialog info
				$('#config-dialog').replaceWith(dialog);
				// check if devices already exist for this configuration TODO
				updateDevicesList($('.devices-list > tbody').html().trim());
				$('#config-dialog').modal('show');
			}
		});
		return false;
	}
	
	// AJAX function to change current configuration
	function setCurrentConfig()
	{
		var id = $(this).attr('data-config');
		var url = sprintf('/configure/set_current_config/%d', id);
		// Send AJAX request
		$.ajax({
			type: 'POST',
			url: url,
			success: updateConfigsList
		});
		return false;
	}
	
	// AJAX function to delete a configuration
	function deleteConfig()
	{
		if (window.confirm('Are you sure you want to remove this configuration?')) {
			var id = $(this).attr('data-config');
			var url = sprintf('/configure/delete_config/%d', id);
			// Send AJAX request
			$.ajax({
				type: 'POST',
				url: url,
				success: updateConfigsList
			});
		}
		return false;
	}
	
	function updateConfigsList(configs)
	{
		if (configs.length == 0) {
			$('.configs-list').hide();
			$('#empty-configs-list').show();
		} else {
			$('#empty-configs-list').hide();
			$('.configs-list > tbody').html(configs);
			// Finally show the configurations list
			$('.configs-list').show();
		}
	}
	
	// AJAX function to save configuration
	function submitConfig()
	{
		console.log('submitConfig()');
		// Submit form alongside map file if provided
		fd = new FormData($('#config_form').get(0));
		$.ajax({
			url: '/configure/save_config',
			type: 'POST',
			data: fd,
			processData: false,
			contentType: false,
			success: function(results) {
				// Check if form submission is valid
				if (results.result === 'OK') {
					// If OK, update config list, flash messages, and hide dialog
					updateConfigsList(results.configs);
					$('#flash-messages').html(results.flash);
					$('#config-dialog').modal('hide');
					//TODO if new config we should go ahead with edit config!!!
				} else {
					// Remove flash messages if any
					$('#flash-messages').html('');
					// Hide dialog before replacing content (otherwise background may stay forever)
					$('#config-dialog').modal('hide');
					// Show form errors by replacing the form
					$('#config-dialog').replaceWith(results.form);
					// Have to show dialog again as replacement hid it
					$('#config-dialog').modal('show');
				}
			}
		});
		return false;
	}
	
	// AJAX function to get form html to create a new device for current configuration
	function openCreateDeviceDialog()
	{
		// Get config id and device kind from clicked link
		var id = $(this).attr('data-config');
		var kind = $(this).attr('data-kind');
		var url = sprintf('/configure/get_new_device_form/%d/%d', id, kind);
		// Get form through AJAX
		$.ajax({
			type: 'GET',
			url: url,
			success: function(form) {
				// Add form to DOM
				$('#device_form').replaceWith(form);
			}
		});
		return false;
	}
	
	// AJAX function to get form html to edit an existing device for current configuration
	function openEditDeviceDialog()
	{
		// Get device id from clicked link
		var id = $(this).attr('data-device');
		var url = sprintf('/configure/get_edit_device_form/%d', id);
		// Get form through AJAX
		$.ajax({
			type: 'GET',
			url: url,
			success: function(form) {
				// Add form to DOM
				$('#device_form').replaceWith(form);
			}
		});
		return false;
	}
	
	// AJAX function to save device
	function submitDevice()
	{
		console.log('submitDevice()');
		// Submit device form
		fd = new FormData($('#device_form').get(0));
		$.ajax({
			url: '/configure/save_device',
			type: 'POST',
			data: fd,
			processData: false,
			contentType: false,
			success: function(results) {
				// Remove flash messages if any
				$('#flash-messages').html('');
				// Check if form submission is valid
				if (results.result === 'OK') {
					// If OK, update devices list and hide device form
					updateDevicesList(results.devices);
					$('#device_form').hide();
				} else {
					// Show form errors by replacing the form
					$('#device_form').replaceWith(results.form);
				}
			}
		});
		return false;
	}
	
	// AJAX function to cancel device edit form
	function cancelDevice()
	{
		$('#device_form').hide();
		return false;
	}
	
	// AJAX function to delete a configuration
	function deleteDevice()
	{
		if (window.confirm('Are you sure you want to remove this module?')) {
			var id = $(this).attr('data-device');
			var url = sprintf('/configure/delete_device/%d', id);
			// Send AJAX request
			$.ajax({
				type: 'POST',
				url: url,
				success: updateDevicesList
			});
		}
		return false;
	}
	
	function updateDevicesList(devices)
	{
		if (devices.length == 0) {
			$('.devices-list').hide();
			$('#empty-devices-list').show();
		} else {
			$('#empty-devices-list').hide();
			$('.devices-list > tbody').html(devices);
			// Finally show the configurations list
			$('.devices-list').show();
		}
	}
	
	// Now get the list of configurations through AJAX
	$.ajax({
		type: 'GET',
		url: '/configure/get_configs_list',
		success: updateConfigsList
	});
	
	// Register event handlers
	// - for list of configurations
	$('.config-new').on('click', openNewConfigDialog);
	$('.configs-list').on('click', '.config-set-current:not(.disabled)', setCurrentConfig);
	$('.configs-list').on('click', '.config-delete', deleteConfig);
	$('.configs-list').on('click', '.config-edit', openEditConfigDialog);
	//TODO missing devices setup in map
	// - for config modal dialog
	$('#modal-content').on('click', '.cancel', function() {
		$('#config-dialog').modal('hide');
	});
	$('#modal-content').on('submit', '#config_form', submitConfig);
	// - for list of modules
	$('#modal-content').on('click', '.create-device', openCreateDeviceDialog);
	$('#modal-content').on('click', '.device-edit', openEditDeviceDialog);
	$('#modal-content').on('click', '.device-delete', deleteDevice);
	// - for device form
	$('#modal-content').on('click', '.device-submit', submitDevice);
	$('#modal-content').on('click', '.device-cancel', cancelDevice);
});
