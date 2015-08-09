$(document).ready(function() {
	//TODO optimize code by using global variables for various jquery selectors
	
	// AJAX function to prepare and open dialog to edit current user's profile
	function openProfileDialog()
	{
		// Send AJAX request
		$.ajax({
			type: 'GET',
			url: '/auth/get_profile',
			success: function(dialog) {
				// update config dialog info
				$('#profile-dialog').replaceWith(dialog);
				$('#profile-dialog').modal('show');
			}
		});
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
	
	// AJAX function to save new profile of current user
	function submitProfile()
	{
		// Submit form alongside map file if provided
		fd = new FormData($('#profile_form').get(0));
		$.ajax({
			url: '/auth/save_profile',
			type: 'POST',
			data: fd,
			processData: false,
			contentType: false,
			success: function(results) {
				// Check if form submission is valid
				if (results.result === 'OK') {
					// If OK, flash messages, and hide dialog
					$('#flash-messages').html(results.flash);
					$('#profile-dialog').modal('hide');
					// update navbar
					$('#nav_username > span').text(results.username);
				} else {
					// Remove flash messages if any
					$('#flash-messages').html('');
					// Hide dialog before replacing content (otherwise background may stay forever)
					$('#profile-dialog').modal('hide');
					// Show form errors by replacing the form
					$('#profile-dialog').replaceWith(results.form);
					// Have to show dialog again as replacement hid it
					$('#profile-dialog').modal('show');
				}
			}
		});
		return false;
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
	$('#modal-content').on('submit', '#profile_form', submitProfile);
	$('#modal-content').on('submit', '#password_form', submitPassword);
});
