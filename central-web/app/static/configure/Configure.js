$(document).ready(function() {
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
	
	function updateConfigsList(results)
	{
		if (results.configs.length == 0) {
			$('.configs-list').hide();
			$('#empty-configs-list').show();
		} else {
			$('#empty-configs-list').hide();
			var $tbody = $('.configs-list > tbody');
			$tbody.html('');
			$tbody.append(results.configs);
			// Register event handlers
			$('.config-set-current').not('.disabled').on('click', setCurrentConfig);
			$('.config-delete').on('click', deleteConfig);
			// Finally show the configurations list
			$('.configs-list').show();
		}
	}
	
	// AJAX function to create new configuration
	function submitCreateConfig(form)
	{
		console.log('submitCreateConfig()');
		// Submit form alongside map file if provided
		fd = new FormData(form);
		$.ajax({
			url: '/configure/create_config_ajax',
			type: 'POST',
			data: fd,
			processData: false,
			contentType: false,
			success: function(results) {
				// Check if form submission is valid
				if (results.result === 'OK') {
					// If OK, hide and clear dialog, update config list
					$('#modal-create-config').modal('hide');
					updateConfigsList(results);
				} else {
					// Get errors and display them in form
					handleErrors('config_', results.fields, results.flash_messages);
				}
			}
		});
		return false;
	}
	
	function handleErrors(formPrefix, fields, messages)
	{
		// Remove previous errors
		clearFormErrors(formPrefix);
		// For each error field, mark the field
		handleFormErrorsInForm(formPrefix, fields);
		// For each message, add a flash message
		handleFlashMessages(messages);
	}
	
	// Now get the list of configurations through AJAX
	$.ajax({
		type: 'GET',
		url: '/configure/get_configs_list',
		success: updateConfigsList
	});

	// Register event handlers
	$('.config-new').on('click', function() {
		$('#config_form').get(0).reset();
		$('#modal-create-config').modal('show');
	});
	$('.cancel').on('click', function() {
		$('#modal-create-config').modal('hide');
	});
	$('#config_form').submit(function(e) {
		submitCreateConfig(this);
		e.preventDefault();
	});
});
