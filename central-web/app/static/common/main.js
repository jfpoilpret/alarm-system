$(document).ready(function() {
	console.log('main.js #1');
	
	//DEBUG ONLY
	function sleepFor( sleepDuration ){
	    var now = new Date().getTime();
	    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ } 
	}
	// Necessary for debugging scripts loaded by $.getScript()
	// http://onwebdev.blogspot.com/2011/08/jquery-getscript-method.html
	$(document).ajaxError(function(e, xhr, settings, exception) {
		console.log('ajaxError #1');
		console.log(e);
		console.log(xhr);
		console.log(exception);
		console.log('ajaxError #2');
	});
	
	// Custom component loader
	var dynamicComponentLoader = {
		getConfig: function(name, callback) {
			callback({ template: name });
		},
		loadTemplate: function(name, config, callback) {
			if (name === 'empty')
				callback([]);
			else
				$.get('/webapp/page', { name: name }).done(function(html) {
					// This is need to convert the resulting html into an array of DOM nodes
					ko.components.defaultLoader.loadTemplate(name, html, callback);
				});
		}
	};
	ko.components.loaders.unshift(dynamicComponentLoader);
	
	// Global ViewModel (should be declared in viewmodel-utils.js and just instantiated here normally)
	// but only if it made more generic, ie more observable components and dict arg for loadFeature
	// children is a dict name -> VM, eventually with undefined or null VM
	function GlobalViewModel(children) {
		var self = this;
		
		self.dialog = { name: ko.observable('empty') };
		self.content = { name: ko.observable('empty') };
		self.navbar = { name: ko.observable('empty') };
		self.flashMessages = new ko.utils.FlashMessagesViewModel();
		$.each(children, function(name, vm) {
			self[name] = ko.observable(vm);
		});

		//TODO Improve: use conventions to calculate complete URL...
		//FIXME need to remove VM that were previously associated with the feature... but how?
		self.loadFeature = function(dialog, content, navbar, scripts) {
			self.dialog.name(dialog || 'empty');
			self.content.name(content || 'empty');
			self.navbar.name(navbar || 'empty');
			// Load script (why not use component?)
			if (scripts) {
				if ($.isArray(scripts)) {
					$.each(scripts, function(index, script) {
						$.getScript(script);
					});
				} else {
					$.getScript(scripts);
				}
			}
		}
		
		self.unload = function() {
			self.loadFeature();
		}
	}
	
	function CurrentUserViewModel() {
		var self = this;
		
		self.id = ko.observable(null);
		self.username = ko.observable();
		self.fullname = ko.observable();
		self.role = ko.observable();
		
		self.isConnected = ko.pureComputed(function() {
			return self.id();
		});
		self.isAdmin = ko.pureComputed(function() {
			return roleIsIn(['Administrator']);
		});
		self.isConfigurator = ko.pureComputed(function() {
			return roleIsIn(['Administrator', 'Configurator']);
		});
		self.isAlarmSetter = ko.pureComputed(function() {
			return roleIsIn(['Administrator', 'Configurator', 'Alarm Setter']);
		});

		var roleIsIn = function(roles) {
			if (self.id())
				return $.inArray(self.role(), roles) != -1;
			else
				return false;
		}
		
		self.update = function(user) {
			if (user) {
				self.id(user.id);
				self.username(user.username);
				self.fullname(user.fullname);
				self.role(user.role);
			} else {
				self.id(null);
				self.username(null);
				self.fullname(null);
				self.role(null);
			}
		}
	}
	
	function NavigationViewModel() {
		var self = this;
		
		self.title = ko.observable('Boulemix');
		
		self.openProfile = function() {
			//TODO
			console.log('openProfile');
		}
		
		self.openPassword = function() {
			//TODO
			console.log('openPassword');
		}
		
		self.gotoAllUsers = function() {
			globalViewModel.loadFeature('/admin/admin_dialogs.html', '/admin/admin_content.html', null, 
					'/static/admin/admin-main.js');
		}
		
		self.gotoConfigure = function() {
			globalViewModel.loadFeature('/configure/configure_dialogs.html', '/configure/configure_content.html', null, 
				['/static/configure/configure-main.js', '/static/configure/configure-svg.js']);
		}
		
		self.gotoMonitor = function() {
			globalViewModel.loadFeature(null, '/monitor/monitor_content.html', '/monitor/monitor_navbar.html',
					'/static/monitor/monitor-main.js');
		}
	}
	
	// Declare VM
	globalViewModel = new GlobalViewModel({
		navigation: new NavigationViewModel(),
		currentUser: new CurrentUserViewModel(),
		signin: null,
		config: null,
		admin: null,
		monitor: null
		//TODO other VM for every feature: Profile, Password...
	});
	ko.applyBindings(globalViewModel);
	
	// Register event handlers
	// - for list of configurations
//	$('#nav_myprofile').on('click', openProfileDialog);
//	$('#nav_mypassword').on('click', userPasswordViewModel.editPassword);
	// - for modal dialog
	$('#modal-content').on('click', '.cancel', function() {
		$('.modal').modal('hide');
	});
	
	// Open login dialog the first time
	globalViewModel.loadFeature('/signin/signin_dialogs.html', null, null, '/static/signin/signin-main.js');
});
