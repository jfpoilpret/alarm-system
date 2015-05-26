
$(document).ready(function() {
	var filterJson = {
		'alert_filter_period_from': $('#alert_filter_period_from').val(),
		'alert_filter_period_to': $('#alert_filter_period_to').val(),
		'alert_filter_alert_level': $('#alert_filter_alert_level').val(),
		'alert_filter_alert_type': $('#alert_filter_alert_type').val()
	};

	// AJAX function to update list with latest (new alerts)
	function refreshAlerts()
	{
		var $tbody = $('.alerts-list > tbody')
		var $latest_id = $('#alert_filter_latest_id');
		// Find the latest alert ID
		filterJson.alert_filter_latest_id = $latest_id.val();
		// Send AJAX request
		$.ajax({
			type: 'POST',
			url: '/monitor/refresh_alerts',
			data: filterJson,
			success: function(results) {
				// Update table on response
				$tbody.prepend(results.alerts);
				// Update latest alert id retrieved also
				$latest_id.val(results.latest_id);
			}
		});
	}
	
	// Automatically refresh alerts on timer every 5 seconds
	var alerts_timer = window.setInterval(refreshAlerts, 5000);

	//TODO Add automatic refresh of maps status
	//TODO Then we should keep only one of these based on the active tab
});
