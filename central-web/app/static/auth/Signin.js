$(document).ready(function() {
	// ViewModel for login dialog
	function LoginViewModel() {
		var self = this;
		self.username = ko.observable();
		self.password = ko.observable();
		self.errors = new ko.errors.ErrorsViewModel([]);
		
		self.reset = function() {
			self.username();
			self.password();
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
				setToken(result.token, result.renew);
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
				flashMessages.clear();
				// Get token and set as basic authentication header
				setToken(result.token, result.renew);
			});
		}
		
		self.reset();
	}
	
	// Declare all VM
	var flashMessages = ko.utils.getFlashMessages($('#flash-messages').get(0));
	var loginViewModel = new LoginViewModel();
	ko.applyBindings(loginViewModel, $('#signin-dialog').get(0));
	
	$('#signin-dialog').modal('show');
});
