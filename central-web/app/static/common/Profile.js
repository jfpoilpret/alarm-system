$(document).ready(function() {
	// Import helpers namespace
	var vmh = viewModelHelpers;
	
	// ViewModel for profile dialog (only)
	function UserProfileViewModel(user) {
		var self = this;
		self.uri = user.uri;
		self.username = ko.observable(user.username);
		self.fullname = ko.observable(user.fullname);
		
		self.toJSON = function() {
			return vmh.extract(self, ['username', 'fullname']);
		}
		
		self.saveProfile = function() {
			var	user = self.toJSON();
			vmh.ajax(self.uri, 'PUT', user).done(function(user) {
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
		self.password1 = ko.observable();
		self.password2 = ko.observable();
		
		self.savePassword = function() {
			// Check both passwords are identical
			if (self.password1() !== self.password2()) {
				//TODO show message
				self.password1('');
				self.password2('');
			} else {
				vmh.ajax(uri, 'PUT', {password: seld.password1()}).done(function(user) {
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
	
	// AJAX function to prepare and open dialog to edit current user's password
	function openPasswordDialog()
	{
		userPasswordViewModel.editPassword();
		return true;
	}
	
	// Register event handlers
	// - for list of configurations
	$('#nav_myprofile').on('click', openProfileDialog);
	$('#nav_mypassword').on('click', openPasswordDialog);
	// - for modal dialog
	$('#modal-content').on('click', '.cancel', function() {
		$('.modal').modal('hide');
	});
});
