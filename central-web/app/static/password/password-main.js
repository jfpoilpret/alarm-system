$(document).ready(function() {
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
					// Add message
					globalViewModel.flashMessages.clear();
					globalViewModel.flashMessages.success('Your password has been changed');
					// Hide dialog
					$('#password-dialog').modal('hide');
				});
			}
		}

		self.editPassword = function() {
			$('#password-dialog').modal('show');
			$('#password_password').focus();
		}
		
		self.install = self.editPassword;
	}
	
	globalViewModel.password(new UserPasswordViewModel());
});
