
$(document).ready(function() {
	var filterJson = {
		'alert_filter_period_from': $('#alert_filter_period_from').val(),
		'alert_filter_period_to': $('#alert_filter_period_to').val(),
		'alert_filter_alert_level': $('#alert_filter_alert_level').val(),
		'alert_filter_alert_type': $('#alert_filter_alert_type').val()
	};
	
	function changeConfigActive(url, message, active)
	{
		if (window.confirm(message)) {
			$.ajax({
				type: 'POST',
				url: url,
				success: function(results) {
					// Update UI
					$('#has_active_configuration').val(active);
					refreshActivation();
				}
			});
		}
		return false;
	}
	
	// AJAX function to activate current config
	function activateConfig()
	{
		return changeConfigActive('/monitor/activate_config', 
			'Are you sure you want to activate the alarm system?', 'true');
	}
	
	// AJAX function to deactivate current config
	function deactivateConfig()
	{
		return changeConfigActive('/monitor/deactivate_config', 
			'Are you sure you want to deactivate the alarm system?', 'false');
	}
	
	function refreshActivation()
	{
		if (isCurrentConfigActive()) {
			$('#activate_config').hide();
			$('#deactivate_config').show();
			$('#config_active').html('Active');
		} else {
			$('#deactivate_config').hide();
			$('#activate_config').show();
			$('#config_active').html('Not Active');
		}
	}
	
	// Function that checks is current configuration is active
	function isCurrentConfigActive()
	{
		return $('#has_active_configuration').val() === 'true';
	}

	// AJAX function to update list with latest (new) alerts
	function refreshAlerts()
	{
		var $tbody = $('.alerts-list > tbody');
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
				// Align column headers width if needed
				alignAlertsListColumns();
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
					var device = results.devices[i];
					var selector = sprintf('#device-%d circle', device.id);
					// Add other information to data content popup?
					var message = sprintf('Voltage: %0.2f V (min.: %0.2f V)\nLatest Ping: %s\n (%d seconds ago)', 
						device.latest_voltage,
						device.voltage_threshold,
						device.latest_ping,
						device.time_since_latest_ping);
					$(selector).attr('data-content', message);
					// Ensure correct refresh of popover if currently displayed
					var idPopover = $(selector).attr('aria-describedby');
					if (idPopover !== undefined) {
						$(selector).popover('show');
					}
					// Change colors based on alerts
					var classes = sprintf('ping-alert-%d voltage-alert-%d', device.ping_alert, device.voltage_alert);
					$(selector).attr('class', classes);
				}
			}
		});
	}
	
	// AJAX function to get requested page of history
	function pageHistory(page)
	{
		var $tbody = $('.history-list > tbody');
		var $pagination = $('#history-pagination');
		var url = sprintf('/monitor/load_history_page/%d', page);
		// Send AJAX request
		$.ajax({
			type: 'GET',
			url: url,
			success: function(results) {
				// Clear previous table body rows
				$tbody.html('');
				// Add paged rows to table body
				$tbody.prepend(results.alerts);
				// Set pagination stuff
				$pagination.html(results.pagination);
				$('[data-page]').on('click', function(e) {
					pageHistory($(this).attr('data-page'));
				});
			}
		});
		return false;
	}
	
	// AJAX function that performs alerts history clear submit
	function clearHistory()
	{
		if (window.confirm('Are you sure you want to clear all alerts?')) {
			// POST form
			var clearJson = {
				'history_clear_clear_until': $('#history_clear_clear_until').val(),
			};
			// Send AJAX request
			$.ajax({
				type: 'POST',
				url: '/monitor/clear_history',
				data: clearJson,
				success: function(results) {
					//TODO do we have some cleanup to perform on the current DOM?
				}
			});
		}
		return false;
	}
	
	// AJAX function that performs alerts filter submit
	function submitAlertsFilter()
	{
		filterJson = {
			'alert_filter_period_from': $('#alert_filter_period_from').val(),
			'alert_filter_period_to': $('#alert_filter_period_to').val(),
			'alert_filter_alert_level': $('#alert_filter_alert_level').val(),
			'alert_filter_alert_type': $('#alert_filter_alert_type').val()
		};
		// Ensure we clear current alerts list first and reload everything that matches filter
		$('.alerts-list > tbody').html('');
		$('#alert_filter_latest_id').val('-1');
		//FIXME issue here is form validation (on server side) and messages display (client side)...
		refreshAlerts();
		return false;
	}

	var $popovers = null;
	
	function clearMapPopups()
	{
		// Before hiding everything first get the list of popovers that are currently displayed!
		$popovers = $('[data-toggle="popover"]').filter(function(index) {
			return $(this).attr('aria-describedby') !== undefined;
		})
	    $popovers.popover('hide');
	}

	function restoreMapPopups()
	{
		// Restore popover that were shown before tab changing
		if ($popovers !== null) {
			$popovers.popover('show');
			$popovers = null;
		}
	}
	
	var alertsListColumnsAligned = false;
	
	function alignAlertsListColumns()
	{
		if (!alertsListColumnsAligned) {
			var $table = $('.alerts-list'),
			$bodyCells = $table.find('tbody tr:first').children(),
			colWidth;
			// Get width of tbody columns
			colWidth = $bodyCells.map(function() {
				return $(this).width();
			}).get();
			// Force width of first column to hard-code value because the one got from tbdoy/tr does not
			// match reality
			colWidth[0] = 14;
			// Set width of thead columns from tbody columns widths
			$table.find('thead tr').children().each(function(i, v) {
				$(v).width(colWidth[i]);
			});
			alertsListColumnsAligned = true;
		}
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
		// Hide all popovers
		if ($(e.target).attr('id') === 'tab_map') {
			clearMapPopups();
		}
	}
	
	function enableTab(e)
	{
		if ($(e.target).attr('id') === 'tab_alerts') {
			// Always refresh alert once immediately, even if no config is active
			refreshAlerts();
		} else if ($(e.target).attr('id') === 'tab_map') {
			// Restore all popovers that were previously shown in the map
			restoreMapPopups();
		} else if ($(e.target).attr('id') === 'tab_history') {
			// Refresh history with pagination
			pageHistory(1);
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
	
	refreshActivation();

	// Register tab event handlers
    $('[data-toggle="popover"]').popover({'container': 'body', 'trigger': 'click', 'placement': 'right'});
	$('a[data-toggle="tab"]').on('hide.bs.tab', disableTab);
	$('a[data-toggle="tab"]').on('shown.bs.tab', enableTab);
	// Register other handlers
	$('#activate_config').on('click', activateConfig);
	$('#deactivate_config').on('click', deactivateConfig);
	$('#history_clear_form').on('submit', clearHistory);
	$('#alert_filter_form').on('submit', submitAlertsFilter);
	// Ensure alerts list header columns widths match content columns after resizing window
	$(window).resize(function() {
		alertsListColumnsAligned = false;
		alignAlertsListColumns();
	});
});
