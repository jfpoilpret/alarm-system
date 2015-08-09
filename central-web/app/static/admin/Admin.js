$(document).ready(function() {
	// Store empty content of form as a way to reset it
	var $newUserForm = $('#user-dialog').clone();

	// Function to show dialog for creating new user
	function openNewEditDialog()
	{
		// Restore form to initial content
		$('#user-dialog').replaceWith($newUserForm.clone());
		$('#user-dialog').modal('show');
		return true;
	}

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
	
	// AJAX function to delete a user
	function deleteUser()
	{
		if (window.confirm('Are you sure you want to remove this user?')) {
			var id = $(this).attr('data-user');
			var url = sprintf('/admin/delete_user/%d', id);
			// Send AJAX request
			$.ajax({
				type: 'POST',
				url: url,
				success: function(results) {
					$('#flash-messages').html(results.flash);
					updateUsersList(results.users);
				}
			});
		}
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
	
	// Now get the list of users through AJAX
	$.ajax({
		type: 'GET',
		url: '/admin/get_users_list',
		success: updateUsersList
	});
	
	// Register event handlers
	// - for list of users
	$('.user-new').on('click', openNewEditDialog);
	$('.users-list').on('click', '.user-delete', deleteUser);
	$('.users-list').on('click', '.user-edit', openEditUserDialog);
	$('.users-list').on('click', '.user-reset-password', resetUserPassword);
	// - for user modal dialog
	$('#modal-content').on('submit', '#user_form', submitUser);
});
