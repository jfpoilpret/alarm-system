$(document).ready(function() {
	// Import helpers namespace
	var vmh = viewModelHelpers;
	
	//TODO missing flash messages if OK (to be done also with KnockOut)
	// ViewModel for user dialog (only)
	function EditUserViewModel() {
		var self = this;
		self.username = ko.observable();
		self.fullname = ko.observable();
		self.password = ko.observable();
		self.role = ko.observable();
		self.isNew = ko.observable();
		self.allRoles = ['Administrator', 'Configurator', 'Alarm Setter', 'Alarm Viewer'];

		var properties = ['username', 'fullname', 'password', 'role'];
		self.errors = new vmh.ErrorsViewModel(properties);
		
		self.toJSON = function() {
			return vmh.extract(self, properties);
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
		}
		
		self.saveUser = function() {
			vmh.ajax(self.uri, 'PUT', self.toJSON()).fail(self.errors.errorHandler).done(function(user) {
				// Signal VM of all users
				usersViewModel.userUpdated(user);
				// Hide dialog
				$('#user-dialog').modal('hide');
			});
		}
		
		self.saveNewUser = function() {
			vmh.ajax('/api/1.0/users', 'POST', self.toJSON()).fail(self.errors.errorHandler).done(function(user) {
				// Signal VM of all users
				usersViewModel.userAdded(user);
				// Hide dialog
				$('#user-dialog').modal('hide');
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
		var compare = vmh.compareByString('username');
		
		// Add additional properties/methods to each user
		self.users = ko.observableArray($.map(users, initUser).sort(compare));
		
		self.editUser = function(user) {
			editUserViewModel.reset(user);
			$('#user-dialog').modal('show');
		}
		
		self.editNewUser = function() {
			// Reset User ViewModel and show dialog
			editUserViewModel.reset();
			$('#user-dialog').modal('show');
		}
		
		self.deleteUser = function(user) {
			if (window.confirm('Are you sure you want to remove this user?')) {
				vmh.ajax(user.uri, 'DELETE').done(function(results) {
					self.users.remove(vmh.filterById(user.id));
				});
			}
		}
		
		self.resetUserPassword = function(user) {
			if (window.confirm('Are you sure you want to reset the password of this user?')) {
				vmh.ajax(user.uri, 'PUT', {password: ''}).done(function(user) {
					//TODO flash
				});
			}
		}
		
		self.userUpdated = function(user) {
			// Replace existing user and re-sort list
			index = vmh.firstIndex(self.users.peek(), vmh.filterById(user.id));
			self.users.peek()[index] = initUser(user);
			self.users.sort(compare);
		}
		
		self.userAdded = function(user) {
			// Add new user and re-sort list
			self.users.push(initUser(user));
			users.sort(compare);
		}
	}
	
	// Declare VM
	var editUserViewModel = new EditUserViewModel();
	ko.applyBindings(editUserViewModel, $('#user-dialog').get(0));

	var usersViewModel;
	// Now get the list of users through AJAX and populate the global VM
	$.getJSON('/api/1.0/users', function(users) {
		usersViewModel = new UsersViewModel(users);
		ko.applyBindings(usersViewModel, $('.users').get(0));
	});
});
