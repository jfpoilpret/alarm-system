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
	}
	
	function handleFlashMessages(messages)
	{
		// For each message, add a flash message
		$('#flash-messages').html(messages);
	}
	
	function handleFormErrors(formPrefix, fields)
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
        exports.handleFormErrors = handleFormErrors
    }
    else {
        window.clearFlashMessages = clearFlashMessages
        window.clearFormErrors = clearFormErrors
        window.handleFlashMessages = handleFlashMessages
        window.handleFormErrors = handleFormErrors

        if (typeof define === "function" && define.amd) {
            define(function() {
                return {
                    clearFlashMessages: clearFlashMessages,
                    clearFormErrors: clearFormErrors,
                    handleFlashMessages: handleFlashMessages,
                    handleFormErrors: handleFormErrors
                }
            })
        }
    }
})(typeof window === "undefined" ? this : window);
