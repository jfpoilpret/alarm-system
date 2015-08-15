$(document).ready(function() {
	// ViewModel for profile dialog (only)
	function UserProfileViewModel(user) {
		var self = this;
		self.uri = user.uri;
		self.username = ko.observable(user.username);
		self.fullname = ko.observable(user.fullname);
		
		var PROPERTIES = ['username', 'fullname'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);
		
		self.toJSON = function() {
			return ko.utils.extract(self, PROPERTIES);
		}

		self.saveProfile = function() {
			var	user = self.toJSON();
			ko.utils.ajax(self.uri, 'PUT', user).fail(self.errors.errorHandler).done(function(user) {
				//TODO How to pass information to users list if currently displayed?
				// Hide dialog
				$('#profile-dialog').modal('hide');
			});
		}

		self.editProfile = function() {
			$('#profile-dialog').modal('show');
		}
	}
	
	// Declare VM
	var userProfileViewModel;
	var uri = sprintf('/api/1.0/users/%s', $('#current-user').val());
	$.getJSON(uri, function(user) {
		userProfileViewModel = new UserProfileViewModel(user);
		ko.applyBindings(userProfileViewModel, $('#profile-dialog').get(0));
	});
	
	// AJAX function to prepare and open dialog to edit current user's profile
	function openProfileDialog()
	{
		userProfileViewModel.editProfile();
		return true;
	}
	
	// ViewModel for password dialog (only)
	function UserPasswordViewModel() {
		var self = this;
		self.password = ko.observable();
		self.password2 = ko.observable();
		
		self.errors = new ko.errors.ErrorsViewModel(['password', 'password2']);
		
		self.savePassword = function() {
			// Check both passwords are identical
			if (self.password() !== self.password2()) {
				// Show error
				self.errors.reset({}, ['Both passwords must be identical']);
				self.password('');
				self.password2('');
			} else {
				ko.utils.ajax(uri, 'PUT', {password: self.password()}).fail(self.errors.errorHandler).done(function(user) {
					// Hide dialog
					$('#password-dialog').modal('hide');
				});
			}
		}

		self.editPassword = function() {
			$('#password-dialog').modal('show');
		}
	}
	
	var userPasswordViewModel = new UserPasswordViewModel();
	ko.applyBindings(userPasswordViewModel, $('#password-dialog').get(0));
		
	// Register event handlers
	// - for list of configurations
	$('#nav_myprofile').on('click', openProfileDialog);
	$('#nav_mypassword').on('click', userPasswordViewModel.editPassword);
	// - for modal dialog
	$('#modal-content').on('click', '.cancel', function() {
		$('.modal').modal('hide');
	});
});
