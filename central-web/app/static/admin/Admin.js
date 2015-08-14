$(document).ready(function() {
	//TODO missing flash messages if OK (to be done also with KnockOut)
	//TODO missing error handling: ajax callback and update dialog form or update flash messages (with KnockOut!)
	function ErrorsViewModel(keys) {
		var self = this;

		self.global = ko.observable('');
		$.each(keys, function(key) {
			self[key] = ko.observable('');
		});

		self.clear = function() {
			$.each(keys, function(key) {
				self[key]('');
			});
			self.global('');
		}
		
		self.reset = function(keyErrors, errors) {
			self.clear();
			$.each(keyErrors, function(key, error) {
				if (self[key] !== undefined) {
					self[key](error);
				} else {
					errors.push(error);
				}
			});
			if (errors) {
				self.global(errors.join('<br>'));
			}
		}
	}
	
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
		self.errors = new ErrorsViewModel(properties);
		
		// Local utility functions (internal use)
		//TODO should it be a function of ErrorsViewModel?
		var errorHandler = function(xhr) {
			var status = xhr.status;
			var result = xhr.responseJSON.message;
			console.log('xhr.status: ' + xhr.status);
			console.log('xhr.responseJSON: ');
			console.log(xhr.responseJSON);
			if (status >= 500) {
				alert(sprintf(
					'A server error %d has occurred:\n%s', status, result));
			} else {
				var errors = [];
				var keyErrors = {};
				if ($.isArray(result)) {
					errors = result;
				} else if ($.isPlainObject(result)) {
					keyErrors = result;
				} else {
					errors = [result];
				}
				self.errors.reset(keyErrors, errors);
			}
		}
		
		self.toJSON = function() {
			return extract(self, properties);
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
		}
		
		self.saveUser = function() {
			ajax(self.uri, 'PUT', self.toJSON()).fail(errorHandler).done(function(user) {
				// Signal VM of all users
				usersViewModel.userUpdated(user);
				// Hide dialog
				$('#user-dialog').modal('hide');
			});
		}
		
		self.saveNewUser = function() {
			ajax('/api/1.0/users', 'POST', self.toJSON()).fail(errorHandler).done(function(user) {
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
		var compare = compareByString('username');
		
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
				ajax(user.uri, 'DELETE').done(function(results) {
					self.users.remove(filterById(user.id));
				});
			}
		}
		
		self.resetUserPassword = function(user) {
			if (window.confirm('Are you sure you want to reset the password of this user?')) {
				ajax(user.uri, 'PUT', {password: ''}).done(function(user) {
					//TODO flash
				});
			}
		}
		
		self.userUpdated = function(user) {
			// Replace existing user and re-sort list
			index = firstIndex(self.users.peek(), filterById(user.id));
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
