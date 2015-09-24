$(document).ready(function() {
	// ViewModel for profile dialog (only)
	function UserProfileViewModel(user) {
		var self = this;
		self.username = ko.observable(user.username);
		self.fullname = ko.observable(user.fullname);
		
		var PROPERTIES = ['username', 'fullname'];
		self.errors = new ko.errors.ErrorsViewModel(PROPERTIES);
		
		var toJSON = function() {
			return ko.utils.extract(self, PROPERTIES);
		}

		self.saveProfile = function() {
			var	user = toJSON();
			ko.utils.ajax(user.uri, 'PUT', user).fail(self.errors.errorHandler).done(function(user) {
				// Update current user data (used in menu bar)
				globalViewModel.currentUser().update(user);
				// Update users list if it is currently visible
				if (globalViewModel.admin()) {
					globalViewModel.admin().userUpdated(user);
				}
				// Hide dialog
				$('#profile-dialog').modal('hide');
				// Add message
				globalViewModel.flashMessages.clear();
				globalViewModel.flashMessages.success('Your profile has been saved');
			});
		}

		self.editProfile = function() {
			$('#profile-dialog').modal('show');
			//NOTE I don't understand why but the following trick is necessary for focus() to work properly
			setTimeout(function() {
				$('#profile_username').focus();
			}, 0);
		}
		
		self.install = self.editProfile;
	}
	
	// Declare VM
	$.getJSON(globalViewModel.currentUser().uri, function(user) {
		globalViewModel.profile(new UserProfileViewModel(user));
	});
});
