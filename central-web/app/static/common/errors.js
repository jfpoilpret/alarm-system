(function(window) {
	// Clear flash messages
	function clearFlashMessages()
	{
		// Remove previous flash messages
		$('#flash-messages').html('');
	}
	
	function clearFormErrors(formPrefix)
	{
		// Remove previous errors from all fields
		$('#' + formPrefix + 'form .form-group').removeClass('has-error');
		$('.help-block').remove();
	}
	
	function handleFlashMessages(messages)
	{
		// For each message, add a flash message
		$('#flash-messages').html(messages);
	}
	
	function handleFormErrorsInForm(formPrefix, fields)
	{
		// For each error field, mark the field
		$.each(fields, function(fieldName, errors) {
			$field = $('#' + formPrefix + fieldName);
			console.log(fieldName);
			type = $field.attr('type');
			if (type !== 'hidden') {
				$group = $field.parent('.form-group');
				$group.addClass('has-error');
				// Add <p> after fields (within same field group)
				$group.append(errors);
			} else {
				// Hidden field: add <p> before all fields
				$('#' + formPrefix + 'form').prepend(errors);
			}
		});
	}
	
	function handleFormErrorsInline(formPrefix, fields)
	{
		// For each error field, mark the field
		$.each(fields, function(index, fieldName) {
			$field = $('#' + formPrefix + fieldName);
			console.log(fieldName);
			type = $field.attr('type');
			if (type !== 'hidden') {
				$field.parent('.form-group').addClass('has-error');
			}
		});
	}
	
    /**
     * export to either browser or node.js
     */
    if (typeof exports !== "undefined") {
        exports.clearFlashMessages = clearFlashMessages
        exports.clearFormErrors = clearFormErrors
        exports.handleFlashMessages = handleFlashMessages
        exports.handleFormErrorsInline = handleFormErrorsInline
        exports.handleFormErrorsInForm = handleFormErrorsInForm
    }
    else {
        window.clearFlashMessages = clearFlashMessages
        window.clearFormErrors = clearFormErrors
        window.handleFlashMessages = handleFlashMessages
        window.handleFormErrorsInline = handleFormErrorsInline
        window.handleFormErrorsInForm = handleFormErrorsInForm

        if (typeof define === "function" && define.amd) {
            define(function() {
                return {
                    clearFlashMessages: clearFlashMessages,
                    clearFormErrors: clearFormErrors,
                    handleFlashMessages: handleFlashMessages,
                    handleFormErrorsInline: handleFormErrorsInline,
                    handleFormErrorsInForm: handleFormErrorsInForm
                }
            })
        }
    }
})(typeof window === "undefined" ? this : window);
