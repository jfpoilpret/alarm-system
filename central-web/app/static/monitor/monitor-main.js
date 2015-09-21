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
		self.activeText = ko.pureComputed(function() {
			return self.active() ? 'Active' : 'Not Active';
		});
		self.lockedText = ko.pureComputed(function() {
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
				alert('A server error ' + status + ' has occurred:\n' + result);
			}
		}
		
		self.refresh = function() {
			$.getJSON('/api/1.0/monitoring/status').done(updateStatusDone).fail(updateStatusFail);
		}
		
		self.errors.clear();
	}

	// Utility function to convert alert level to CSS class
	function alertLevelClass(level) {
		var ALERT_LEVEL_CLASS = {
				'info': 'info-sign',	
				'warning': 'exclamation-sign',	
				'alarm': 'exclamation-sign',	
			};
		return 'alert-level-' + level + ' glyphicon glyphicon-' + ALERT_LEVEL_CLASS[level];
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
		self.alerts = ko.observableArray();
		self.alertLevelClass = alertLevelClass;
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
			if (alert || self.alerts().length)
				alignAlertsListColumns();
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
		self.title = 'Module ' + device.name + ' (ID ' + device.id + ')';
		self.alertClasses = ko.observable('ping-alert-ok voltage-alert-ok');

		self.update = function(dev) {
			// Update content and alertClasses
			var voltage = (dev.latest_voltage ? dev.latest_voltage.toFixed(2) : '??');
			var message =	'Voltage: ' + voltage + ' V (min.: ' + dev.voltage_threshold.toFixed(2) + 
							' V)\nLatest Ping: ' + moment(dev.latest_ping).format('DD-MM-YYYY HH:mm:ss') + '\n (' +
							dev.time_since_latest_ping + ' seconds ago)';
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
		self.url = ko.pureComputed(function() {
			return '/api/1.0/history/' + statusMonitor.id() + '/alerts'
		});
		self.alerts = ko.observable();
		self.alertLevelClass = alertLevelClass;
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

		// Internal utility functions, used by event handlers
		var $popovers = null;
		var clearMapPopups = function() {
			// Before hiding everything first get the list of popovers that are currently displayed!
			$popovers = $('[data-toggle="popover"][aria-describedby*="popover"]');
		    $popovers.popover('hide');
		};
		var restoreMapPopups = function() {
			// Restore popover that were shown before tab changing
			if ($popovers !== null) {
				$popovers.popover('show');
				$popovers = null;
			}
		}

		// Event handlers
		//================
		// We enable only one refresh timer, based on current active tab
		var disableTab = function(e) {
			if (self.statusMonitor.active()) {
				if ($(e.target).attr('id') === 'tab_map') {
					self.mapMonitor.autoRefresh(false);
				} else if ($(e.target).attr('id') === 'tab_alerts') {
					self.alertsMonitor.autoRefresh(false);
				}
			}
			// Hide all popovers
			if ($(e.target).attr('id') === 'tab_map') {
				clearMapPopups();
			}
		}
		var enableTab = function(e) {
			targetTab = $(e.target).attr('id');
			if (targetTab === 'tab_alerts') {
				// Always refresh alert once immediately, even if no config is active
				self.alertsMonitor.refresh();
			} else if (targetTab === 'tab_map') {
				// Restore all popovers that were previously shown in the map
				restoreMapPopups();
			} else if (targetTab === 'tab_history') {
				// Refresh history with pagination
				//FIXME this loses latest page visited everytime we switch tabs!
				self.alertsHistory.refresh();
			}
			if (self.statusMonitor.active()) {
				if (targetTab === 'tab_map') {
					self.mapMonitor.refresh();
					self.mapMonitor.autoRefresh(true);
				} else if (targetTab === 'tab_alerts') {
					self.alertsMonitor.autoRefresh(true);
				}
			}
		}

		// Lifecycle
		//===========
		self.uninstall = function() {
			// Stop all refresh timers
			self.statusMonitor.autoRefresh(false);
			self.alertsMonitor.autoRefresh(false);
			self.mapMonitor.autoRefresh(false);
			// Unregister all event handlers
			$('a[data-toggle="tab"]').off('hide.bs.tab', disableTab);
			$('a[data-toggle="tab"]').off('shown.bs.tab', enableTab);
			$(window).off('resize', alignAlertsListColumns);
			// Hide all popovers 
			$('[data-toggle="popover"]').popover('hide');
		}
		self.install = function() {
			// Force first refresh and start refresh timer
			self.statusMonitor.refresh();
			self.statusMonitor.autoRefresh(true);
			self.alertsMonitor.refresh();
			self.mapMonitor.init();
			// NOTE: we have to defer the following because DOM is asynchronously updated by mapMonitor.init()
			$(document).ready(function() {
				// Register all event handlers
				$('a[data-toggle="tab"]').on('hide.bs.tab', disableTab);
				$('a[data-toggle="tab"]').on('shown.bs.tab', enableTab);
				$(window).on('resize', alignAlertsListColumns);
				// Force control tab active
				$('#tab_control').tab('show');
			});
		}
	}
	
	var monitor = new MonitoringViewModel();
	globalViewModel.monitor(monitor);
	
	function alignAlertsListColumns() {
		ko.utils.alignTableColumns('.alerts-list');
	}
});
