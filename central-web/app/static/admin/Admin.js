$(document).ready(function() {
	//TODO use only one ViewModel with everything instead of a hierarchy?
	//TODO missing flash messages if OK (to be done also with KnockOut)
	//TODO missing error handling: ajax callback and update dialog form or update flash messages (with KnockOut!)
	
	//=======================================//
	// REFACTORING WITH KNOCKOUT STARTS HERE //
	//=======================================//

	// Utilities
	//==========
	function extract(item, keys, includeUndefined) {
		item = ko.toJS(item);
		var result = {};
		for (var key in item) {
			if ($.inArray(key, keys) > -1) {
				var value = item[key];
				if (includeUndefined || value !== undefined) {
					result[key] = value;
				}
			}
		}
		return result;
	}
	
    function ajax(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            accepts: "application/json",
            cache: false
        };
        if (data !== undefined) {
            request.contentType = "application/json";
            request.dataType = 'json';
        	request.data = JSON.stringify(data); 
        }
        return $.ajax(request);
    }
	
    function firstIndex(list, predicate) {
    	var firstIndex = -1;
    	$.grep(list, function(item, index) {
    		if (predicate(item) && (firstIndex == -1))
    			firstIndex = index;
    		return false;
    	});
    	return firstIndex;
    }
    
	// ViewModels
	//============
	// ViewModel for user dialog (only)
	function UserViewModel(user) {
		var self = this;
		
		self.username = ko.observable();
		self.fullname = ko.observable();
		self.password = ko.observable();
		self.role = ko.observable();
		self.isNew = ko.observable();
		
		self.allRoles = ['Administrator', 'Configurator', 'Alarm Setter', 'Alarm Viewer'];
		
		self.toJSON = function() {
			return extract(self, ['username', 'fullname', 'password', 'role']);
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
					role: 'Alert Viewer'
				};
			}
			self.id = newUser.id;
			self.uri = newUser.uri;
			self.username(newUser.username);
			self.fullname(newUser.fullname);
			//TODO deal with user objects without password (ie not new users)
			self.password(newUser.password);
			self.role(newUser.role);
			self.isNew(isNew);
		}
		
		self.reset(user);
	}
	
	function UsersViewModel(currentUser, users, editUserVM) {
		var self = this;
		
		self.editUserViewModel = editUserVM;
		
		// Local utility functions (internal use)
		var filter = function(id) {
			return function(user) {
				return user.id == id;
			}
		}
		
		var compare = function(user1, user2) {
			if (user1.username === user2.username) return 0;
			return user1.username < user2.username ? -1 : +1;
		}
		
		var initUser = function(user) {
			user.canBeDeleted = (user.id !== currentUser);
			return user;
		}
		
		// Add additional properties/methods to each user VM?
		var count = users.length;
		for (var i = 0; i < count; i++) {
			users[i] = initUser(users[i]);
		}
//		// Make each individual user an observable (as a whole)
//		self.users = ko.observableArray($.map(users, function(user) {
//			return ko.observable(user);
//		}));
		self.users = ko.observableArray(users.sort(compare));
		
		self.editUser = function(user) {
			//TODO
			console.log('editUser');
			console.log(user);
			self.editUserViewModel.reset(user);
			$('#user-dialog').modal('show');
		}
		
		self.editNewUser = function() {
			// Reset User ViewModel and show dialog
			self.editUserViewModel.reset();
			$('#user-dialog').modal('show');
		}
		
		self.deleteUser = function(user) {
			if (window.confirm('Are you sure you want to remove this user?')) {
				// Send AJAX request
				ajax(user.uri, 'DELETE').done(function(results) {
					self.users.remove(filter(user.id));
				});
			}
			return true;
		}
		
		self.resetUserPassword = function(user) {
			//TODO
			console.log('resetUserPassword');
			console.log(user);
		}
		
		self.saveUser = function() {
			var	vm = self.editUserViewModel, 
				user = vm.toJSON();
			ajax(vm.uri, 'PUT', user).done(function(user) {
				// Replace existing user
				user = initUser(user);
				index = firstIndex(self.users.peek(), filter(user.id));
				self.users.peek()[index] = user;
				// Sort array!
				self.users.sort(compare);
				// Hide dialog
				$('#user-dialog').modal('hide');
			});
		}
		
		self.saveNewUser = function() {
			var	user = self.editUserViewModel.toJSON();
			ajax('/api/1.0/users', 'POST', user).done(function(user) {
				// Add new user
				self.users.push(initUser(user));
				// Sort array!
				self.users.sort(compare);
				// Hide dialog
				$('#user-dialog').modal('hide');
			});
		}
	} 
	
	function GlobalViewModel(users) {
		var self = this;
		
		//TODO Add CSRF token here?
		self.currentUser = Number($('#current-user').val());
		self.editedUser = new UserViewModel();
		self.allUsers = new UsersViewModel(self.currentUser, users, self.editedUser);
	}
	
	// Declare VM
	var globalViewModel;
	
	// Now get the list of users through AJAX and populate the global VM
	$.getJSON('/api/1.0/users', function(users) {
		globalViewModel = new GlobalViewModel(users);
		ko.applyBindings(globalViewModel);
	});

/*
	// AJAX function to prepare and open dialog to edit user
	function openEditUserDialog()
	{
		// Load data for this user
		var id = $(this).attr('data-user');
		var url = sprintf('/admin/get_user/%d', id);
		// Send AJAX request
		$.ajax({
			type: 'GET',
			url: url,
			success: function(dialog) {
				// update edit dialog info
				$('#user-dialog').replaceWith(dialog);
				$('#user-dialog').modal('show');
			}
		});
		return true;
	}
	
	// AJAX function to reset a user's password
	function resetUserPassword()
	{
		if (window.confirm('Are you sure you want to reset the password of this user?')) {
			var id = $(this).attr('data-user');
			var url = sprintf('/admin/reset_user_password/%d', id);
			// Send AJAX request
			$.ajax({
				type: 'POST',
				url: url,
				success: function(results) {
					$('#flash-messages').html(results.flash);
				}
			});
		}
		return true;
	}
	
*/
});
