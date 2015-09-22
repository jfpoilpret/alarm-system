$(document).ready(function() {
	// ViewModel for user dialog (only)
	function EditUserViewModel() {
		var self = this;
		self.username = ko.observable();
		self.fullname = ko.observable();
		self.password = ko.observable();
		self.role = ko.observable();
		self.isNew = ko.observable();
		self.allRoles = ['Administrator', 'Configurator', 'Alarm Setter', 'Alarm Viewer'];

		var PROPERTIES = ['username', 'fullname', 'password', 'role'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);
		self.dirtyFlag = new ko.utils.VMDirtyFlag(self);
		
		self.toJSON = function() {
			return ko.utils.extract(self, PROPERTIES);
		}

		self.reset = function(newUser) {
			self.user = newUser;
			var isNew = (newUser === undefined);
			if (isNew) {
				newUser = {
					id: undefined,
					uri: undefined,
					username: undefined,
					fullname: undefined,
					password: undefined,
					role: self.allRoles[self.allRoles.length - 1]
				};
			}
			self.id = newUser.id;
			self.uri = newUser.uri;
			self.username(newUser.username);
			self.fullname(newUser.fullname);
			self.password(newUser.password);
			self.role(newUser.role);
			self.isNew(isNew);
			self.errors.clear();
			self.dirtyFlag.reset();
		}
		
		self.saveUser = function() {
			ko.utils.ajax(self.uri, 'PUT', self.toJSON()).fail(self.errors.errorHandler).done(function(user) {
				// Signal VM of all users
				globalViewModel.admin().userUpdated(user);
				// Hide dialog
				$('#user-dialog').modal('hide');
				// Add message
				globalViewModel.flashMessages.clear();
				globalViewModel.flashMessages.success('User \'' + user.username + '\' has been saved');
			});
		}
		
		self.saveNewUser = function() {
			ko.utils.ajax('/api/1.0/users', 'POST', self.toJSON()).fail(self.errors.errorHandler).done(function(user) {
				// Signal VM of all users
				globalViewModel.admin().userAdded(user);
				// Hide dialog
				$('#user-dialog').modal('hide');
				// Add message
				globalViewModel.flashMessages.clear();
				globalViewModel.flashMessages.success('New user \'' + user.username + '\' has been created');
			});
		}
		
		self.reset();
	}
	
	function UsersViewModel(users) {
		var self = this;
		
		// Local utility functions (internal use)
		var currentUser = Number($('#current-user').val());
		var initUser = function(user) {
			user.canBeDeleted = (user.id !== currentUser);
			return user;
		}
		var compare = ko.utils.compareByString('username');
		
		// Add additional properties/methods to each user
		self.users = ko.observableArray($.map(users, initUser).sort(compare));
		
		self.userEditor = new EditUserViewModel();
		
		self.editUser = function(user) {
			self.userEditor.reset(user);
			$('#user-dialog').modal('show');
			$('#user_username').focus();
		}
		
		self.editNewUser = function() {
			// Reset User ViewModel and show dialog
			self.userEditor.reset();
			$('#user-dialog').modal('show');
			$('#user_username').focus();
		}
		
		self.deleteUser = function(user) {
			if (window.confirm('Are you sure you want to remove this user?')) {
				ko.utils.ajax(user.uri, 'DELETE').done(function(results) {
					self.users.remove(ko.utils.filterById(user.id));
					// Add message
					globalViewModel.flashMessages.clear();
					globalViewModel.flashMessages.success('User \'' + user.username + '\' has been removed');
				});
			}
		}
		
		self.resetUserPassword = function(user) {
			if (window.confirm('Are you sure you want to reset the password of this user?')) {
				ko.utils.ajax(user.uri, 'PUT', {password: ''}).done(function(user) {
					// Add message
					globalViewModel.flashMessages.clear();
					globalViewModel.flashMessages.success('Password of user \'' + user.username + '\' has been reset');
				});
			}
		}
		
		self.userUpdated = function(user) {
			// Replace existing user and re-sort list
			index = ko.utils.firstIndex(self.users.peek(), ko.utils.filterById(user.id));
			self.users.peek()[index] = initUser(user);
			self.users.sort(compare);
		}
		
		self.userAdded = function(user) {
			// Add new user and re-sort list
			self.users.push(initUser(user));
			self.users.sort(compare);
		}
	}
	
	// Create main VM (and children hierarchy) for configuration
	$.getJSON('/api/1.0/users', function(users) {
		globalViewModel.admin(new UsersViewModel(users));
	});
});
