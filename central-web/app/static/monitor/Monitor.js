
$(document).ready(function() {
	var filterJson = {
		'alert_filter_period_from': $('#alert_filter_period_from').val(),
		'alert_filter_period_to': $('#alert_filter_period_to').val(),
		'alert_filter_alert_level': $('#alert_filter_alert_level').val(),
		'alert_filter_alert_type': $('#alert_filter_alert_type').val()
	};

	// AJAX function to update list with latest (new) alerts
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
	
	// AJAX function to update device state on monitoring map
	function refreshMap()
	{
		// Send AJAX request
		$.ajax({
			type: 'POST',
			url: '/monitor/refresh_devices',
			success: function(results) {
				// Update map (SVG) on response
				for (var i = 0; i < results.devices.length; i++) {
					device = results.devices[i];
					selector = sprintf('#device-%d circle', device.id);
					//TODO Add other information to data content popup?
					message = sprintf('Voltage: %0.2f V\nLatest Ping: %s', 
						device.latest_voltage,
						device.latest_ping);
					$(selector).attr('data-content', message);
					// Change colors based on alerts
					classes = sprintf('ping-alert-%d voltage-alert-%d', device.ping_alert, device.voltage_alert);
					$(selector).attr('class', classes);
				}
				//FIXME there seems to be no refresh of SVG after class changes!
			}
		});
	}

	// Automatically refresh alerts on timer every 5 seconds
//	refreshAlerts();
//	var alerts_timer = window.setInterval(refreshAlerts, 5000);
	refreshMap();
	var map_timer = window.setInterval(refreshMap, 5000);

	function disableTab(e)
	{
		//TODO
		console.log('disableTab');
		console.log(e.target);
	}
	
	function enableTab(e)
	{
		//TODO
		console.log('enableTab');
		console.log(e.target);
	}

	// Register tab event handlers
	$('a[data-toggle="tab"]').on('hide.bs.tab', disableTab);
	$('a[data-toggle="tab"]').on('shown.bs.tab', enableTab);
	
	//TODO Then we should keep only one of these based on the active tab
});
