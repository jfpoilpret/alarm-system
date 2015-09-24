$(document).ready(function() {
	console.log('main.js #1');
	
	//DEBUG ONLY
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
	// - components: array of KO components that can be replaced when loading a feature
	// - features: list of all available features (each feature has one VM assigned with its name)
	//		those VM get reset whenever loadPersistentFeature() is called
	// - viewModels: additional dict of viewModels that do not belong to features and never get reset automatically
	function GlobalViewModel(components, features, viewModels) {
		var self = this;

		// Handle components
		$.each(components, function(index, name) {
			self[name] = { name: ko.observable('empty') };
		});
		
		// Handlers to handle lifecycle of children ViewModels
		var beforeChange = function(vm) {
			// Check vm is not null and includes a uninstall() function
			if (vm && vm.uninstall) vm.uninstall();
		};
		var afterChange = function(vm) {
			// Check vm is not null and includes a install() function
			if (vm && vm.install) {
				$(document).ready(vm.install);
			}
		};
		$.each(features, function(index, name) {
			var obs = ko.observable(null);
			self[name] = obs;
			// Add subscribers to change in order to manage lifecycle of old/new VM
			obs.subscribe(beforeChange, null, 'beforeChange');
			obs.subscribe(afterChange, null, 'change');
		});
		$.each(viewModels, function(name, vm) {
			self[name] = ko.observable(vm);
		});
		self.flashMessages = new ko.utils.FlashMessagesViewModel();

		self.clearFeatures = function() {
			$.each(features, function(index, feature) {
				self[feature](null);
			});
		}

		// Load a feature after clearing previously loaded feature
		self.loadPersistentFeature = function(componentsContent, feature, scripts) {
			// Clear all previous features, transient or persistent
			self.clearFeatures();
			self.loadTransientFeature(componentsContent, feature, scripts)
		}
		
		// Load a feature without clearing previously loaded feature, this allows e.g. to show a transient
		// dialog above the current feature without needing to reload current feature once dialog is finished using.
		self.loadTransientFeature = function(componentsContent, feature, scripts) {
			console.log('loadFeature() -> ' + feature);
			// First clear flash messages and ensure demanded feature is removed if present already
			self.flashMessages.clear();
			self[feature](null);
			// Set all required components
			var prefix = '/' + feature + '/' + feature;
			$.each(componentsContent, function(name, content) {
				if (content)
					content = prefix + '_' + content + '.html';
				console.log('    ' + name + ' -> ' + content);
				self[name].name(content || 'empty');
			});
			if (scripts && !$.isArray(scripts))
				scripts = [scripts];
			prefix = '/static' + prefix + '-';
			$.each(scripts, function(index, script) {
				script = prefix + script + '.js';
				console.log('    script -> ' + script);
				$.getScript(script);
			});
		}
	}
	
	function CurrentUserViewModel() {
		var self = this;
		
		self.uri = null;
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
				self.uri = user.uri;
				self.id(user.id);
				self.username(user.username);
				self.fullname(user.fullname);
				self.role(user.role);
			} else {
				self.uri = null;
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
			globalViewModel.loadTransientFeature(transientComponents(), 'profile', 'main');
		}
		self.openPassword = function() {
			globalViewModel.loadTransientFeature(transientComponents(), 'password', 'main');
		}
		self.gotoAllUsers = function() {
			globalViewModel.loadPersistentFeature(persistentComponents(true, true), 'admin', 'main');
		}
		self.gotoConfigure = function() {
			globalViewModel.loadPersistentFeature(persistentComponents(true, true), 'configure', ['main', 'svg']);
		}
		self.gotoMonitor = function() {
			globalViewModel.loadPersistentFeature(persistentComponents(false, true, true), 'monitor', 'main');
		}
		self.logout = function() {
			$.ajax('/api/1.0/security/token', {
				method: 'DELETE'
			}).always(function() {
				globalViewModel.currentUser().update(null);
				location.reload(true);
			});
		}
	}
	
	// Declare VM
	globalViewModel = new GlobalViewModel(
		['navbar', 'content', 'dialog1', 'dialog2'], 
		['signin', 'configure', 'admin', 'monitor', 'profile', 'password'], 
		{
			navigation: new NavigationViewModel(),
			currentUser: new CurrentUserViewModel()
		});
	ko.applyBindings(globalViewModel);
	
	// Register general event handler for modal dialog
	$('#modal-content').on('click', '.cancel', function() {
		$('.modal').modal('hide');
	});

	// Utility functions to help create arguments for loadPersistentFeature/loadTransientFeature
	function persistentComponents(dialog, content, navbar) {
		return {
			dialog1: (dialog ? 'dialogs' : null),
			dialog2: null,
			content: (content ? 'content' : null),
			navbar: (navbar ? 'navbar' : null)
		};
	}
	function transientComponents() {
		return {
			dialog2: 'dialogs'
		};
	}
	
	// Open login dialog the first time
	globalViewModel.loadPersistentFeature(persistentComponents(true), 'signin', 'main');
});
