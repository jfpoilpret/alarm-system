
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
			$('.config-set-current').not('.disabled').on('click', setCurrentConfig);
			$('.config-delete').on('click', deleteConfig);
			$('.configs-list').show();
		}
	}
	
	// Now get the list of configurations through AJAX
	$.ajax({
		type: 'GET',
		url: '/configure/get_configs_list',
		success: updateConfigsList
	});
});
