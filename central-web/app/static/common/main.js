$(document).ready(function() {
	console.log('main.js #1');
	
	//DEBUG ONLY
	function sleepFor( sleepDuration ){
	    var now = new Date().getTime();
	    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ } 
	}
	
	// Custom component loader
	var dynamicComponentLoader = {
		getConfig: function(name, callback) {
//			console.log('getConfig -> ' + name);
			callback({ template: name });
		},
		loadTemplate: function(name, config, callback) {
//			console.log('loadTemplate -> ' + name);
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
		self.flashMessages = new ko.utils.FlashMessagesViewModel();
		$.each(children, function(name, vm) {
			self[name] = ko.observable(vm);
		});

		self.loadFeature = function(dialog, content, script) {
			self.dialog.name(dialog || 'empty');
			self.content.name(content || 'empty');
			//TODO load script (why not use component?)
			if (script)
				$.getScript(script);
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
			//TODO
			console.log('gotoAllUsers');
		}
		
		self.gotoConfigure = function() {
			//TODO
			console.log('gotoConfigure');
		}
		
		self.gotoMonitor = function() {
			//TODO
			console.log('gotoMonitor');
		}
	}
	
	// Declare VM
	globalViewModel = new GlobalViewModel({
		navigation: new NavigationViewModel(),
		currentUser: new CurrentUserViewModel(),
		signin: null
		//TODO other VM for every feature: Signin, Users, Configure, Monitor, Profile, Password...
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
	
	//TODO Open login dialog the first time
//	sleepFor(2000);
	globalViewModel.loadFeature('/signin/signin_dialogs.html', null, '/static/signin/signin-main.js');
	// 1. Load signin dialog HTML
//	$('#modal-content').load('/webapp/page', 'name=/signin/signin_dialogs.html', function() {
//		// 2. Load and execute signin JS
//		$.getScript('/static/signin/signin-main.js');
//	});

	//TODO generic method to load a "feature":
	// - unload previous feature (from DOM and from GlobalViewModel)
	// - load new feature (DOM content and dialogs, JS file, load & execute, link new VMs to GlobalVM)

});
