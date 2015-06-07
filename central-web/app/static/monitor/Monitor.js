
$(document).ready(function() {
	var filterJson = {
		'alert_filter_period_from': $('#alert_filter_period_from').val(),
		'alert_filter_period_to': $('#alert_filter_period_to').val(),
		'alert_filter_alert_level': $('#alert_filter_alert_level').val(),
		'alert_filter_alert_type': $('#alert_filter_alert_type').val()
	};
	
	// Function that checks is current configuration is active
	function isCurrentConfigActive()
	{
		//FIXME actually this is incorrect as the deactivate button exists only for users 
		// in role ALARM_SETTER and above!
		// => update home.html to add hidden field only for active configuration
		return $('#deactivate_config').length > 0;
	}

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
					// Ensure correct refresh of popover if currently displayed
					idPopover = $(selector).attr('aria-describedby');
					if (idPopover !== undefined) {
						$(selector).popover('show');
					}
					// Change colors based on alerts
					classes = sprintf('ping-alert-%d voltage-alert-%d', device.ping_alert, device.voltage_alert);
					$(selector).attr('class', classes);
				}
			}
		});
	}

	// Automatically refresh map on timer every 5 seconds
	var map_timer = null;
	var alerts_timer = null;
	if (isCurrentConfigActive()) {
		refreshMap();
		map_timer = window.setInterval(refreshMap, 5000);
	}

	// We enable only one refresh timer, based on current active tab
	function disableTab(e)
	{
		if (isCurrentConfigActive()) {
			if ($(e.target).attr('id') === 'tab_map') {
				if (map_timer !== null) {
					window.clearInterval(map_timer);
					map_timer = null;
				}
			} else if ($(e.target).attr('id') === 'tab_alerts') {
				if (alerts_timer !== null) {
					window.clearInterval(alerts_timer);
					alerts_timer = null;
				}
			}
		}
	}
	
	function enableTab(e)
	{
		if ($(e.target).attr('id') === 'tab_alerts') {
			// Always refresh alert once immediately, even if no config is active
			refreshAlerts();
		}
		if (isCurrentConfigActive()) {
			if ($(e.target).attr('id') === 'tab_map') {
				refreshMap();
				map_timer = window.setInterval(refreshMap, 5000);
			} else if ($(e.target).attr('id') === 'tab_alerts') {
				alerts_timer = window.setInterval(refreshAlerts, 5000);
			}
		}
	}

	// Register tab event handlers
	$('a[data-toggle="tab"]').on('hide.bs.tab', disableTab);
	$('a[data-toggle="tab"]').on('shown.bs.tab', enableTab);
});
