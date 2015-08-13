$(document).ready(function() {
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
            request.dataType: 'json';
        	request.data = JSON.stringify(data); 
        }
        return $.ajax(request);
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
		
		self.toJSON = function() {
			return extract(self, ['username', 'fullname', 'password', 'role']);
		}
		
		self.replace = function(newUser) {
			self.isNew = (newUser === undefined);
			if (self.isNew) {
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
		}
		
		self.replace(user);
	}
	
	function UsersViewModel(currentUser, users, editUserVM) {
		var self = this;
		
		self.editUserViewModel = editUserVM;
		
		var filter = function(id) {
			return function(user) {
				return user.id == id;
			}
		}
		
		// Add additional properties/methods to each user VM?
		var count = users.length;
		for (var i = 0; i < count; i++) {
			var user = users[i];
			user.canBeDeleted = (user.id !== currentUser);
		}
		self.users = ko.observableArray(users);
		
		self.editUser = function(user) {
			//TODO
			console.log('editUser');
			console.log(user);
		}
		
		self.editNewUser = function() {
			// Reset User ViewModel and show dialog
			self.editUserViewModel.replace();
			$('#user-dialog').modal('show');
		}
		
		self.deleteUser = function(user) {
			if (window.confirm('Are you sure you want to remove this user?')) {
				// Send AJAX request
				//TODO Handle errors!
				ajax(user.uri, 'DELETE').done(function(results) {
					self.users.remove(filter(user.id));
					//TODO directly manage flash messages...
//						$('#flash-messages').html(results.flash);
				});
//				$.ajax({
//					type: 'DELETE',
//					url: user.uri,
//					success: function(results) {
//						self.users.remove(filter(user.id));
//						//TODO directly manage flash messages...
////						$('#flash-messages').html(results.flash);
//					}
//				});
			}
			return true;
		}
		
		self.resetUserPassword = function(user) {
			//TODO
			console.log('resetUserPassword');
			console.log(user);
		}
		
		self.saveUser = function() {
			//TODO
			console.log('saveUser');
			var isNew = self.editUserViewModel.isNew;
			var uri = isNew ? '/api/1.0/users' : self.editUserViewModel.uri;
			var method = isNew ? 'POST' : 'PUT';
			var user = self.editUserViewModel.toJSON();
			console.log(user);
			ajax(uri, method, user).done(function(user) {
				if (isNew) {
					self.users.push(user);
				} else {
					self.users.replace()
				}
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
	// Function to show dialog for creating new user
	function openNewEditDialog()
	{
		var user = {
			id: null, 
			username: null, 
			fullname: null, 
			password: null, 
			role: 'Alarm Viewer', 
			uri: null
		};
		//TODO Bind empty model to the dialog
		if (userViewModel === undefined) {
			// Initialize and bind ViewModel
			//TODO Need special mapping?
			userViewModel = ko.mapping.fromJS(user);
			// Add new functions to ViewModel?
			//TODO
			// Bind ViewModel
			ko.applyBindings(userViewModel, $('#user-dialog').get(0));
		} else {
			// Update ViewModel
			ko.mapping.fromJS(user, userViewModel);
		}
		// Restore form to initial content
		$('#user-dialog').modal('show');
		return true;
	}

	// AJAX function to save user
	function submitUser()
	{
		console.log('submitUser');
		user = ko.mapping.toJS(userViewModel);
		console.log(user);
		// Check if this is a new user or not
		var	method = 'POST', 
			uri = '/api/1.0/users';
		if (user.id !== null) {
			method = 'PUT';
			uri = user.uri;
			// password is never submitted when editing user
			delete user.password;
		}
		// Remove additional properties that should not be POSTed
		delete user.id;
		delete user.uri;
		$.ajax({
			url: uri,
			type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(user),
			success: function(user) {
				//TODO handler erros in another callback...
				// If OK, update users list, flash messages, and hide dialog
				usersViewModel.users.mappedCreate(user);
//				updateUsersList(results.users);
//				$('#flash-messages').html(results.flash);
				$('#user-dialog').modal('hide');
			}
		});
		return false;
	}

	// AJAX function to delete a user
	function deleteUser()
	{
		if (window.confirm('Are you sure you want to remove this user?')) {
			var $parent = $(this).closest('tr');
			var id = $parent.attr('data-user-id');
			var uri = $parent.attr('data-user-uri');
			console.log('deleteUser');
			console.log(uri);
			// Send AJAX request
			$.ajax({
				type: 'DELETE',
				url: uri,
				success: function(results) {
					//FIXME THAT does not work...
					list = usersViewModel.users.mappedRemove({id: id});
					console.log(list);
					//TODO directly manage flash messages...
//					$('#flash-messages').html(results.flash);
//					updateUsersList3(results.users);
				}
			});
		}
		return true;
	}
*/	

	//======================================//
	// REFACTORING WITH KNOCKOUT ENDS THERE //
	//======================================//
	
	//TODO Generic functions should be factored out
	function listToDict(list, id)
	{
		var dict = {};
		$.each(list, function(index, value) {
			dict[value[id]] = value;
		});
		return dict;
	}
	
	function dictToList(dict)
	{
		var list = [];
		$.each(dict, function(key, value) {
			list.push(value);
		});
		return list;
	}
	
	function fillForm(form, prefix, data)
	{
		//TODO
	}
	
	// Store empty content of form as a way to reset it
	var $newUserForm = $('#user-dialog').clone();
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
	
	function updateUsersList(users)
	{
		$('.users-list > tbody').html(users);
	}
	
	var allUsers = {};
	
	function updateUsersList2(users)
	{
		allUsers = listToDict(users, 'id');
		// render JSON with nunjucks
//		var usersHtml = nunjucks.render('all_user_rows.html', {users: users});
		var usersHtml = nunjucks.render(
			'all_user_rows.html', {current_user_id: currentUserId, users: dictToList(allUsers)});
		$('.users-list > tbody').html(usersHtml);
	}
*/
/*
	// AJAX function to save user
	function submitUser()
	{
		// Submit form alongside map file if provided
		fd = new FormData($('#user_form').get(0));
		$.ajax({
			url: '/admin/save_user',
			type: 'POST',
			data: fd,
			processData: false,
			contentType: false,
			success: function(results) {
				// Check if form submission is valid
				if (results.result === 'OK') {
					// If OK, update users list, flash messages, and hide dialog
					updateUsersList(results.users);
					$('#flash-messages').html(results.flash);
					$('#user-dialog').modal('hide');
				} else {
					// Remove flash messages if any
					$('#flash-messages').html('');
					// Hide dialog before replacing content (otherwise background may stay forever)
					$('#user-dialog').modal('hide');
					// Show form errors by replacing the form
					$('#user-dialog').replaceWith(results.form);
					// Have to show dialog again as replacement hid it
					$('#user-dialog').modal('show');
				}
			}
		});
		return true;
	}
*/
	
	// Initialize nunjucks
//	nunjucks.configure('/static/views', {autoescape: true});
	
	// Register event handlers
	// - for list of users
//	$('.user-new').on('click', openNewEditDialog);
//	$('.users-list').on('click', '.user-delete', deleteUser);
//	$('.users-list').on('click', '.user-edit', openEditUserDialog);
//	$('.users-list').on('click', '.user-reset-password', resetUserPassword);
	// - for user modal dialog
//	$('#modal-content').on('submit', '#user_form', submitUser);
});
