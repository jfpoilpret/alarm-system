$(document).ready(function() {
	// ViewModel for login dialog
	function LoginViewModel() {
		var self = this;
		self.username = ko.observable();
		self.password = ko.observable();
		self.errors = new ko.errors.ErrorsViewModel([], false);
		
		self.reset = function() {
			self.username(null);
			self.password(null);
			self.errors.clear();
		}
		
		var setToken = function(token, renew) {
			// Set token in header for all next ajax calls
			$.ajaxSetup({
				beforeSend: function(xhr) {
					xhr.setRequestHeader('Authorization', 'Basic ' + window.btoa(token + ':'));
				} 
			});
			// Set timer for refreshing token
			window.setTimeout(refreshToken, renew * 1000);
		}
		
		var refreshToken = function() {
			$.ajax('/api/1.0/security/token', {
			}).fail(function(xhr) {
				var status = xhr.status;
				var result = xhr.responseJSON.message;
				console.log('refreshToken() fail (' + status + ', ' + result + ')');
				if (status === 401) {
					// Automatically show signin
					location.reload(true);
				} else {
					alert('A server error ' + status + ' has occurred:\n' + result);
				}
			}).done(function(result) {
				// Get token and set as basic authentication header
				setToken(result.token, result.renew_before);
			});
		}
		
		self.signIn = function() {
			$.ajax('/api/1.0/security/token?token_only=false', {
				beforeSend: function(xhr) {
					xhr.setRequestHeader('Authorization', 'Basic ' + window.btoa(
						self.username() + ':' + self.password()));
				} 
			}).fail(self.errors.errorHandler).done(function(result) {
				// Hide dialog
				$('#signin-dialog').modal('hide');
				// Add message
				globalViewModel.flashMessages.clear();
				// Get token and set as basic authentication header
				setToken(result.token, result.renew_before);
				// Update current user VM
				globalViewModel.currentUser().update(result.user);
				// Load next feature based on current user role
				if (globalViewModel.currentUser().isConfigurator())
					globalViewModel.navigation().gotoConfigure();
				else
					globalViewModel.navigation().gotoMonitor();
			});
		}
		
		self.install = function() {
			self.reset();
			$('#signin-dialog').modal('show');
			$('#signin_username').focus();
		}
	}
	
	// Set login VM into Global VM and (automatically) show login dialog
	globalViewModel.signin(new LoginViewModel());
});
