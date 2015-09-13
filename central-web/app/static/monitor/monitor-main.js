$(document).ready(function() {
	// Utility function used in most ViewModel
	function autoRefresh(timer, refresh, callback, period) {
		if (refresh && timer === null) {
			// Start timer
			return window.setInterval(callback, period);
		} else if (timer !== null && !refresh) {
			// Stop timer
			window.clearInterval(timer);
			return null;
		}
		return timer;
	}
	
	// ViewModel in charge of status update (auto-refresh) for title bar and control tab
	function StatusViewModel() {
		var self = this;
		
		self.id = ko.observable();
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
			timer = autoRefresh(timer, refresh, self.refresh, 5000);
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
			changeStatus('Are you sure you want to activate the alarm system?', { active: true });
		}
		self.deactivate = function() {
			changeStatus('Are you sure you want to deactivate the alarm system?', { active: false });
		}
		self.lock = function() {
			changeStatus('Are you sure you want to lock the alarm?', { locked: true });
		}
		self.unlock = function() {
			changeStatus('Are you sure you want to unlock the alarm?', { locked: false });
		}
		
		var changeStatus = function(message, status) {
			if (window.confirm(message)) {
				ko.utils.ajax('/api/1.0/monitoring/status', 'PUT', status).
					done(updateStatusDone).fail(updateStatusFail);
			}
		}
		var updateStatusDone = function(status) {
			self.id(status.id);
			if (status.name !== self.name()) {
				self.name(status.name);
				// Update map
				monitor.mapMonitor.init();
				//TODO update other models?
			}
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
		
		self.errors.clear();
	}

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
			timer = autoRefresh(timer, refresh, self.refresh, 5000);
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
		
		self.errors.clear();
	}

	function DeviceViewModel(device, r) {
		var self = this;

		self.id = device.id;
		self.x = device.x;
		self.y = device.y;
		self.r = r;
		self.content = ko.observable();
		self.title = sprintf('Module %s (ID %d)', device.name, device.id);
		self.alertClasses = ko.observable('ping-alert-ok voltage-alert-ok');

		self.update = function(dev) {
			// Update content and alertClasses
			var message = sprintf('Voltage: %0.2f V (min.: %0.2f V)\nLatest Ping: %s\n (%d seconds ago)', 
				dev.latest_voltage,
				dev.voltage_threshold,
				moment(dev.latest_ping).format('DD-MM-YYYY HH:mm:ss'),
				dev.time_since_latest_ping);
			self.content(message);
			var css = 'ping-alert-' + (dev.ping_alert || 'ok');
			css = css + ' voltage-alert-' + (dev.voltage_alert || 'ok');
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
			timer = autoRefresh(timer, refresh, self.refresh, 5000);
		}
		
		var updateDevice = function(index, source) {
			var targets = $.grep(self.devices(), function(device) { return source.id === device.id; });
			if (targets.length > 0)
				targets[0].update(source);
			// Ensure popover are refreshed if currently shown
			$('[data-toggle="popover"][aria-describedby*="popover"]').popover('show');
		}
		var updateDevicesDone = function(devices) {
			$.each(devices, updateDevice);
		}
		
		self.refresh = function() {
			$.getJSON('/api/1.0/monitoring/devices', updateDevicesDone);
		}
		
	}

	function AlertsHistoryViewModel(statusMonitor) {
		var self = this;
		
		// Pagination
		self.has_prev = ko.observable();
		self.has_next = ko.observable();
		self.iter_pages = ko.observable();
		self.page = ko.observable();
		self.pages = ko.observable();
		// Alerts list
		self.url = ko.computed(function() {
			//FIXME monitor() is null at construction time!
			return '/api/1.0/history/' + statusMonitor.id() + '/alerts'
		});
		self.alerts = ko.observable();
		//TODO refactor (common with AlertsViewModel)
		var ALERT_LEVEL_CLASS = {
			'info': 'info-sign',	
			'warning': 'exclamation-sign',	
			'alarm': 'exclamation-sign',	
		};
		self.alertLevelClass = function(level) {
			return 'alert-level-' + level + ' glyphicon glyphicon-' + ALERT_LEVEL_CLASS[level];
		}
		self.alertTime = function(when) {
			return moment(when).format('DD-MM-YYYY HH:mm:ss');
		}
		
		// Pagination handlers
		var historyLoadDone = function(result) {
			self.has_prev(result.has_prev);
			self.has_next(result.has_next);
			self.page(result.page);
			self.pages(result.pages);
			self.iter_pages(result.iter_pages);
			self.alerts(result.alerts);
		}
		
		self.firstPage = function() { self.gotoPage(1); }
		self.lastPage = function() { self.gotoPage(self.pages()); }
		self.gotoPage = function(page) {
			$.getJSON(self.url(), { page: page }).done(historyLoadDone);
		}
		
		self.refresh = function() {
			self.gotoPage(1);
		}
	}
	
	function MonitoringViewModel() {
		var self = this;
		
		self.statusMonitor = new StatusViewModel();
		self.alertsMonitor = new AlertsViewModel();
		self.mapMonitor = new MapViewModel();
		self.alertsHistory = new AlertsHistoryViewModel(self.statusMonitor);
		
		self.init = function() {
			self.statusMonitor.refresh();
			self.statusMonitor.autoRefresh(true);
			self.alertsMonitor.refresh();
			self.mapMonitor.init();
		}
	}
	
	var monitor = new MonitoringViewModel();
	globalViewModel.monitor(monitor);
	// Initialize the model only after it has been added to Global VM
	monitor.init();
	
	var $popovers = null;
	function clearMapPopups() {
		// Before hiding everything first get the list of popovers that are currently displayed!
		$popovers = $('[data-toggle="popover"][aria-describedby*="popover"]');
	    $popovers.popover('hide');
	}
	function restoreMapPopups() {
		// Restore popover that were shown before tab changing
		if ($popovers !== null) {
			$popovers.popover('show');
			$popovers = null;
		}
	}
	
	var alertsListColumnsAligned = false;
	function alignAlertsListColumns() {
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
	function disableTab(e) {
		if (monitor.statusMonitor.active()) {
			if ($(e.target).attr('id') === 'tab_map') {
				monitor.mapMonitor.autoRefresh(false);
			} else if ($(e.target).attr('id') === 'tab_alerts') {
				monitor.alertsMonitor.autoRefresh(false);
			}
		}
		// Hide all popovers
		if ($(e.target).attr('id') === 'tab_map') {
			clearMapPopups();
		}
	}
	function enableTab(e) {
		targetTab = $(e.target).attr('id');
		if (targetTab === 'tab_alerts') {
			// Always refresh alert once immediately, even if no config is active
			monitor.alertsMonitor.refresh();
		} else if (targetTab === 'tab_map') {
			// Restore all popovers that were previously shown in the map
			restoreMapPopups();
		} else if (targetTab === 'tab_history') {
			// Refresh history with pagination
			//FIXME this loses latest page visited everytime we switch tabs!
			monitor.alertsHistory.refresh();
		}
		if (monitor.statusMonitor.active()) {
			if (targetTab === 'tab_map') {
				monitor.mapMonitor.refresh();
				monitor.mapMonitor.autoRefresh(true);
			} else if (targetTab === 'tab_alerts') {
				monitor.alertsMonitor.autoRefresh(true);
			}
		}
	}

	// Register tab event handlers
	$('a[data-toggle="tab"]').on('hide.bs.tab', disableTab);
	$('a[data-toggle="tab"]').on('shown.bs.tab', enableTab);
	
	// Ensure alerts list header columns widths match content columns after resizing window
	$(window).resize(function() {
		alertsListColumnsAligned = false;
		alignAlertsListColumns();
	});
	
	// Force control tab active
	$('#tab_control').tab('show');
});
