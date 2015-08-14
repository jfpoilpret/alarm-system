$(document).ready(function() {
	// ViewModels
	//============
	// ViewModel for profile dialog (only)
	function UserProfileViewModel(user) {
		var self = this;
		self.uri = user.uri;
		self.username = ko.observable(user.username);
		self.fullname = ko.observable(user.fullname);
		
		self.toJSON = function() {
			return extract(self, ['username', 'fullname']);
		}
		
		self.saveProfile = function() {
			var	user = self.toJSON();
			ajax(self.uri, 'PUT', user).done(function(user) {
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
	console.log('profile.js');
	console.log(uri);
	$.getJSON(uri, function(user) {
		console.log('getJSON');
		console.log(user);
		userProfileViewModel = new UserProfileViewModel(user);
		ko.applyBindings(userProfileViewModel, $('#profile-dialog').get(0));
	});
	
	// AJAX function to prepare and open dialog to edit current user's profile
	function openProfileDialog()
	{
		userProfileViewModel.editProfile();
		return true;
	}
	
	// AJAX function to prepare and open dialog to edit current user's password
	function openPasswordDialog()
	{
		// Send AJAX request
		$.ajax({
			type: 'GET',
			url: '/auth/get_password',
			success: function(dialog) {
				// update config dialog info
				$('#password-dialog').replaceWith(dialog);
				$('#password-dialog').modal('show');
			}
		});
		return true;
	}
	
	// AJAX function to save new password of current user
	function submitPassword()
	{
		//TODO
		// Submit form alongside map file if provided
		fd = new FormData($('#password_form').get(0));
		$.ajax({
			url: '/auth/save_password',
			type: 'POST',
			data: fd,
			processData: false,
			contentType: false,
			success: function(results) {
				$('#flash-messages').html(results.flash);
				// Check if form submission is valid
				if (results.result === 'OK') {
					// If OK, hide dialog
					$('#password-dialog').modal('hide');
				} else if (results.form) {
					// Hide dialog before replacing content (otherwise background may stay forever)
					$('#password-dialog').modal('hide');
					// Show form errors by replacing the form
					$('#password-dialog').replaceWith(results.form);
					// Have to show dialog again as replacement hid it
					$('#password-dialog').modal('show');
				}
			}
		});
		return false;
	}
	
	// Register event handlers
	// - for list of configurations
	$('#nav_myprofile').on('click', openProfileDialog);
	$('#nav_mypassword').on('click', openPasswordDialog);
	// - for modal dialog
	$('#modal-content').on('click', '.cancel', function() {
		$('.modal').modal('hide');
	});
//	$('#modal-content').on('submit', '#profile_form', submitProfile);
	$('#modal-content').on('submit', '#password_form', submitPassword);
});
