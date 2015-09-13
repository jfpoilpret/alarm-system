$(document).ready(function() {
	// ViewModel for login dialog
	function LoginViewModel() {
		var self = this;
		self.username = ko.observable();
		self.password = ko.observable();
		self.errors = new ko.errors.ErrorsViewModel([]);
		
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
			// Use the following line instead when debugging security
//			window.setTimeout(refreshToken, 60 * 1000);
		}
		
		var refreshToken = function() {
			$.ajax('/api/1.0/security/token', {
			}).fail(self.errors.errorHandler).done(function(result) {
				console.log(result);
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
				console.log(result);
				// Hide dialog
				$('#signin-dialog').modal('hide');
				// Add message
				globalViewModel.flashMessages.clear();
				// Get token and set as basic authentication header
				setToken(result.token, result.renew_before);
				//TODO Update VM of current user (navigation)
				globalViewModel.currentUser().update(result.user);
				//TODO Load next feature based on current user role
			});
		}

		console.log('LoginViewModel');
		self.reset();
	}
	
	console.log('signin-main.js #1a');
	console.log('signin-main.js #1b');
	// Declare all VM
	console.log(globalViewModel);
	globalViewModel.signin(new LoginViewModel());
	console.log('signin-main.js #2');
	$('#signin-dialog').modal('show');
	console.log('signin-main.js #3');
});
