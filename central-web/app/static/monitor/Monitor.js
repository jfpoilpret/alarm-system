$(document).ready(function() {
	//TODO Refactoring step by step
	// 4. VM for history
	
	// ViewModel in charge of status update (auto-refresh) for title bar and control tab
	function StatusViewModel() {
		var self = this;
		
		self.name = ko.observable();
		self.active = ko.observable();
		self.locked = ko.observable();
		self.activeText = ko.computed(function() {
			return self.active() ? 'Active' : 'Not Active';
		});
		self.lockedText = ko.computed(function() {
			if (self.active())
				return self.locked() ? ' - Locked' : ' - Unlocked';
			else
				return '';
		});

		// Form to clear history
		self.clear_until = ko.observable();
		// Errors
		var PROPERTIES = ['clear_until'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);
		
		var timer = null;

		self.autoRefresh = function(refresh) {
			if (refresh && timer === null) {
				// Start timer
				timer = window.setInterval(self.refresh, 5000);
			} else if (timer !== null && !refresh) {
				// Stop timer
				window.clearInterval(timer);
				timer = null;
			}
		}
		
		// Click handlers
		self.clearHistory = function() {
			if (window.confirm('Are you sure you want to clear all alerts?')) {
				var url = '/api/1.0/monitoring/alerts?' + $.param({ clear_until: self.clear_until() });
				$.ajax({
					url: url,
					method: 'DELETE',
				}).fail(self.errors.errorHandler).done(function() {
					// Clear history form
					self.clear_until(null);
					//TODO LATER clear all alerts viewmodels
				});
			}
		}
		self.activate = function() {
			return changeStatus('Are you sure you want to activate the alarm system?', { active: true });
		}
		self.deactivate = function() {
			return changeStatus('Are you sure you want to deactivate the alarm system?', { active: false });
		}
		self.lock = function() {
			return changeStatus('Are you sure you want to lock the alarm?', { locked: true });
		}
		self.unlock = function() {
			return changeStatus('Are you sure you want to unlock the alarm?', { locked: false });
		}
		
		var changeStatus = function(message, status) {
			if (window.confirm(message)) {
				ko.utils.ajax('/api/1.0/monitoring/status', 'PUT', status).
					done(updateStatusDone).fail(updateStatusFail);
			}
			return false;
		}
		var updateStatusDone = function(status) {
			self.name(status.name);
			self.active(status.active);
			self.locked(status.locked);
		}
		var updateStatusFail = function(xhr) {
			var status = xhr.status;
			var result = xhr.responseJSON.message;
			if (status === 404) {
				self.name(null);
				self.active(null);
				self.locked(null);
			} else if (status >= 500) {
				alert(sprintf(
					'A server error %d has occurred:\n%s', status, result));
			}
		}
		
		self.refresh = function() {
			$.getJSON('/api/1.0/monitoring/status').done(updateStatusDone).fail(updateStatusFail);
		}
		
		// Force 1st refresh immediately
		self.refresh();
		self.errors.clear();
	}

	var statusViewModel = new StatusViewModel();
	ko.applyBindings(statusViewModel, $('#status').get(0));
	ko.applyBindings(statusViewModel, $('#control').get(0));
	statusViewModel.autoRefresh(true);
	
	function AlertsViewModel() {
		var self = this;
		
		// filter form
		self.period_from = ko.observable();
		self.period_to = ko.observable();
		self.alert_level = ko.observable();
		self.alert_type = ko.observable();
		// select options
		self.allAlertLevels = [
   			{ code: undefined, label: 'All Levels'},
			{ code: 'info', label: 'Info'},
			{ code: 'warning', label: 'Warning'},
			{ code: 'alarm', label: 'Alarm'}];
		self.allAlertTypes = [
			{ code: undefined, label: 'All Alerts'}, 
			{ code: 'no-ping', label: 'Missing Pings'}, 
			{ code: 'voltage-level', label: 'Voltage Level'}, 
			{ code: 'lock', label: 'Alarm Lock'}, 
			{ code: 'unlock', label: 'Alarm Unlock'}, 
			{ code: 'activation', label: 'Alarm Activation'}, 
			{ code: 'deactivation', label: 'Alarm Deactivation'}, 
			{ code: 'wrong-code', label: 'Wrong Code'}];

		// Errors
		var PROPERTIES = ['period_from', 'period_to', 'alert_level', 'alert_type'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);

		// alerts table
		var ALERT_LEVEL_CLASS = {
			'info': 'info-sign',	
			'warning': 'exclamation-sign',	
			'alarm': 'exclamation-sign',	
		};
		self.alerts = ko.observableArray();
		self.alertLevelClass = function(level) {
			return 'alert-level-' + level + ' glyphicon glyphicon-' + ALERT_LEVEL_CLASS[level];
		}
		self.alertTime = function(when) {
			return moment(when).format('DD-MM-YYYY HH:mm:ss');
		}
		
		var filter = {
			since_id: undefined,
			period_from: undefined,
			period_to: undefined,
			alert_level: undefined,
			alert_type: undefined
		};
		
		self.filterAlerts = function() {
			var newFilter = {
				since_id: undefined,
				period_from: self.period_from(),
				period_to: self.period_to(),
				alert_level: self.alert_level(),
				alert_type: self.alert_type()
			};
			// Refresh with new filter
			self.refresh(newFilter, function(alerts) {
				filter = newFilter;
				self.alerts([]);
				updateAlertsDone(alerts);
			});
		}
		self.resetAlerts = function() {
			self.period_from(undefined);
			self.period_to(undefined);
			self.alert_level(undefined);
			self.alert_type(undefined);
			// Submit filter again
			self.filterAlerts();
		}
		
		var timer = null;

		self.autoRefresh = function(refresh) {
			if (refresh && timer === null) {
				// Start timer
				timer = window.setInterval(self.refresh, 5000);
			} else if (timer !== null && !refresh) {
				// Stop timer
				window.clearInterval(timer);
				timer = null;
			}
		}
		
		var updateAlertsDone = function(alerts) {
			var alert;
			var len = alerts.length;
			for (var i = 0; i < len; i++) {
				alert = alerts[len - i - 1];
				self.alerts.unshift(alert);
			}
			if (alert)
				filter.since_id = alert.id;
		}
		
		self.refresh = function(newFilter, done) {
			newFilter = newFilter || filter;
			done = done || updateAlertsDone;
			$.getJSON('/api/1.0/monitoring/alerts', newFilter).done(done).fail(self.errors.errorHandler);
		}
		
		// Force 1st refresh immediately
		self.errors.clear();
		self.refresh();
	}

	var alertsViewModel = new AlertsViewModel();
	ko.applyBindings(alertsViewModel, $('#alerts').get(0));
//	alertsViewModel.autoRefresh(true);

	//TODO handle popover here?
	function DeviceViewModel(device, r) {
		var self = this;

		self.id = device.id;
		self.x = device.x;
		self.y = device.y;
		self.r = r;
		self.content = ko.observable();
		self.title = sprintf('Module %s (ID %d)', device.name, device.id);
		self.alertClasses = ko.observable('ping-alert-ok voltage-alert-ok');

		self.update = function(device) {
			// Update content and alertClasses
			var message = sprintf('Voltage: %0.2f V (min.: %0.2f V)\nLatest Ping: %s\n (%d seconds ago)', 
				device.latest_voltage,
				device.voltage_threshold,
				device.latest_ping,
				device.time_since_latest_ping);
			self.content(message);
			var css = 'ping-alert-' + (device.ping_alert || 'ok');
			css = css + ' voltage-alert-' + (device.voltage_alert || 'ok');
			self.alertClasses(css);
		}
	}
	
	function MapViewModel() {
		var self = this;
		
		self.backgroundMap = ko.observable();
		self.width = ko.observable();
		self.height = ko.observable();
		self.viewBox = ko.observable();
		self.devices = ko.observableArray();
		
		self.init = function() {
			// Get map + devices info from server
			//TODO errors handling
			$.getJSON('/api/1.0/monitoring/map', function(result) {
				self.devices([]);
				self.backgroundMap(result.map);
				self.width(result.width);
				self.height(result.height);
				self.viewBox(result.viewBox);
				var devices = $.map(result.devices, function(device) {
					return new DeviceViewModel(device, result.r)
				})
				self.devices(devices);
			    $('[data-toggle="popover"]').popover({'container': 'body', 'trigger': 'click', 'placement': 'right'});
			});
		}
		
		var timer = null;

		self.autoRefresh = function(refresh) {
			if (refresh && timer === null) {
				// Start timer
				timer = window.setInterval(self.refresh, 5000);
			} else if (timer !== null && !refresh) {
				// Stop timer
				window.clearInterval(timer);
				timer = null;
			}
		}
		
		var updateDevice = function(index, source) {
			var targets = $.grep(self.devices(), function(device) { return source.id === device.id; });
			if (targets.length > 0)
				targets[0].update(source);
			
		}
		var updateDevicesDone = function(devices) {
			$.each(devices, updateDevice);
		}
		
		self.refresh = function() {
			$.getJSON('/api/1.0/monitoring/devices', updateDevicesDone);
		}
		
	}

	var mapViewModel = new MapViewModel();
	ko.applyBindings(mapViewModel, $('#map').get(0));
	mapViewModel.init();
//	mapViewModel.autoRefresh(true);
	
//	function updateStatus(results)
//	{
//		// Only update if changes sicne last call
//		if (results.hashcode != lastStatusHash) {
//			console.log('updateStatus()');
//			
//			if (results.namehash != lastConfigNameHash) {
//				// Reload map if needed
//				lastConfigNameHash = results.namehash;
//				reloadMap();
//			}
//		}
//	}
//	
//	// AJAX function to update device state on monitoring map
//	function refreshMap()
//	{
//		// Send AJAX request
//		$.ajax({
//			type: 'POST',
//			url: '/monitor/refresh_devices',
//			success: function(results) {
//				// Update map (SVG) on response
//				for (var i = 0; i < results.devices.length; i++) {
//					var device = results.devices[i];
//					var selector = sprintf('#device-%d circle', device.id);
//					// Add other information to data content popup?
//					var message = sprintf('Voltage: %0.2f V (min.: %0.2f V)\nLatest Ping: %s\n (%d seconds ago)', 
//						device.latest_voltage,
//						device.voltage_threshold,
//						device.latest_ping,
//						device.time_since_latest_ping);
//					$(selector).attr('data-content', message);
//					// Ensure correct refresh of popover if currently displayed
//					var idPopover = $(selector).attr('aria-describedby');
//					if (idPopover !== undefined) {
//						$(selector).popover('show');
//					}
//					// Change colors based on alerts
//					var classes = sprintf('ping-alert-%d voltage-alert-%d', device.ping_alert, device.voltage_alert);
//					$(selector).attr('class', classes);
//				}
//			}
//		});
//	}
//	
//	// AJAX function to get requested page of history
//	function pageHistory(page)
//	{
//		var $tbody = $('.history-list > tbody');
//		var $pagination = $('#history-pagination');
//		var url = sprintf('/monitor/load_history_page/%d', page);
//		// Send AJAX request
//		$.ajax({
//			type: 'GET',
//			url: url,
//			success: function(results) {
//				// Clear previous table body rows
//				$tbody.html('');
//				// Add paged rows to table body
//				$tbody.prepend(results.alerts);
//				// Set pagination stuff
//				$pagination.html(results.pagination);
//				$('[data-page]').on('click', function(e) {
//					pageHistory($(this).attr('data-page'));
//				});
//			}
//		});
//		return false;
//	}
	
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
			var	$table = $('.alerts-list'),
				$bodyCells = $table.find('tbody tr:first').children();
			// Resize only if there is at least one row
			if ($bodyCells.length > 0) {
				// Get width of tbody columns
				var colWidth = $bodyCells.map(function() {
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
	}

	// We enable only one refresh timer, based on current active tab
	function disableTab(e)
	{
		if (statusViewModel.active()) {
			if ($(e.target).attr('id') === 'tab_map') {
				mapViewModel.autoRefresh(false);
			} else if ($(e.target).attr('id') === 'tab_alerts') {
				alertsViewModel.autoRefresh(false);
			}
		}
		// Hide all popovers
		if ($(e.target).attr('id') === 'tab_map') {
			clearMapPopups();
		}
	}
	
	function enableTab(e)
	{
		targetTab = $(e.target).attr('id');
		if (targetTab === 'tab_alerts') {
			// Always refresh alert once immediately, even if no config is active
			alertsViewModel.refresh();
		} else if (targetTab === 'tab_map') {
			// Restore all popovers that were previously shown in the map
			restoreMapPopups();
//		} else if (targetTab === 'tab_history') {
//			// Refresh history with pagination
//			pageHistory(1);
		}
		if (statusViewModel.active()) {
			if (targetTab === 'tab_map') {
				mapViewModel.refresh();
				mapViewModel.autoRefresh(true);
			} else if (targetTab === 'tab_alerts') {
				alertsViewModel.autoRefresh(true);
			}
		}
//		// Keep track of latest tab in current URL so that refresh will go to the last visible tab
//		window.history.replaceState(targetTab, targetTab, '/monitor/home?tab=' + targetTab);
	}

	// Register tab event handlers
	$('a[data-toggle="tab"]').on('hide.bs.tab', disableTab);
	$('a[data-toggle="tab"]').on('shown.bs.tab', enableTab);
	
	// Ensure alerts list header columns widths match content columns after resizing window
	$(window).resize(function() {
		alertsListColumnsAligned = false;
		alignAlertsListColumns();
	});
	
//	// Force active tab based on current active_tab
//	activeTab = $('#active_tab').val();
//	$('#' + activeTab).tab('show');
});
