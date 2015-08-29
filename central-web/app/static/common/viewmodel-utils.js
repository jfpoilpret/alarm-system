(function(window) {
	function extract(item, keys, includeUndefined) {
		item = ko.toJS(item);
		var result = {};
		for (var key in item) {
			if ($.inArray(key, keys) > -1) {
				var value = item[key];
				if (includeUndefined || value !== undefined) {
					result[key] = value;
				}
			}
		}
		return result;
	}
	
    function ajax(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            accepts: "application/json",
            cache: false
        };
        if (data !== undefined) {
            request.contentType = "application/json";
            request.dataType = 'json';
        	request.data = JSON.stringify(data); 
        }
        return $.ajax(request);
    }
    
    function range(min, max, step) {
    	var result = [];
    	if (!step) step = 1;
    	for (var i = min; i < max; i += step) result.push(i);
    	return result;
    }

    //TODO Check if we can directly extend observableArray with this function
    function firstIndex(list, predicate) {
    	var firstIndex = -1;
    	$.grep(list, function(item, index) {
    		if (predicate(item) && (firstIndex == -1))
    			firstIndex = index;
    		return false;
    	});
    	return firstIndex;
    }
    
	function filterById(id) {
		return function(item) {
			return item.id == id;
		}
	}
    
	function compareByString(attribute) {
		return function(item1, item2) {
			var value1 = item1[attribute],
				value2 = item2[attribute];
			if (value1 === value2) return 0;
			return value1 < value2 ? -1 : +1;
		}
	}
	
	function compareByNumber(attribute) {
		return function(item1, item2) {
			var value1 = item1[attribute],
				value2 = item2[attribute];
			if (value1 === value2) return 0;
			return value1 < value2 ? -1 : +1;
		}
	}
	
	// ViewModel for form errors
	function ErrorsViewModel(keys) {
		var self = this;

		keys = keys || [];
		self.global = ko.observable('');
		$.each(keys, function(index, key) {
			self[key] = ko.observable('');
		});

		self.clear = function() {
			$.each(keys, function(index, key) {
				self[key]('');
			});
			self.global('');
		}
		
		self.reset = function(keyErrors, errors) {
			self.clear();
			$.each(keyErrors, function(key, error) {
				if (keys.indexOf(key) > -1) {
					self[key](error);
				} else {
					errors.push(error);
				}
			});
			if (errors) {
				self.global(errors.join('<br>'));
			}
		}
		
		self.errorHandler = function(xhr) {
			var status = xhr.status;
			var result = xhr.responseJSON.message;
			if (status >= 500) {
				alert(sprintf(
					'A server error %d has occurred:\n%s', status, result));
			} else {
				var errors = [];
				var keyErrors = {};
				if ($.isArray(result)) {
					errors = result;
				} else if ($.isPlainObject(result)) {
					keyErrors = result;
				} else {
					errors = [result];
				}
				self.reset(keyErrors, errors);
			}
		}
	}
	
	// ViewModel for flash messages
	function FlashMessagesViewModel() {
		var self = this;
		self.messages = ko.observableArray();
		
		self.clear = function(alert) {
			if (alert) 
				self.messages.remove(alert);
			else
				self.messages.removeAll();
		}
		
		var ALERT_TYPES = {
			success: { alertClass: 'alert-success',	iconClass: 'glyphicon-ok-sign' },
			info:	 { alertClass: 'alert-info',	iconClass: 'glyphicon-info-sign' },
			warning: { alertClass: 'alert-warning',	iconClass: 'glyphicon-exclamation-sign' },
			error:	 { alertClass: 'alert-danger',	iconClass: 'glyphicon-exclamation-sign' }
		};

		var addMessage = function(message, type) {
			var alertType = ALERT_TYPES[type];
			self.messages.push({
				message: message,
				alertClass: alertType.alertClass,
				iconClass: alertType.iconClass
			});
		}
		
		self.success = function(message) {
			addMessage(message, 'success');
		}
		self.info = function(message) {
			addMessage(message, 'info');
		}
		self.warning = function(message) {
			addMessage(message, 'warning');
		}
		self.error = function(message) {
			addMessage(message, 'error');
		}
	}
	
	var flashMessages;
	
	// Function to create a dirty flag on a list of observables
	//TODO Then improve to allow either a list of observable or a whole ViewModel (simple common cases)
	function DirtyFlag(observables) {
		var self = this,
			// IMPORTANT! Note the trick [value()] to ensure $.map() will keep null values in the resulting array
			_initialState = $.map(observables, function(value) { return [value()]; }),
			_initiallyDirty = ko.observable(false);

		_initiallyDirty.extend({ notify: 'always' });
		
		self.isDirty = ko.computed(function() {
			var changes = 0,
				len = observables.length;
			for (var i = 0; i < len; i++) {
				if (_initialState[i] !== observables[i]()) {
					changes++;
				}
			}
			return _initiallyDirty() || changes !== 0;
		});
		
		self.reset = function(initiallyDirty) {
			// IMPORTANT! Note the trick [value()] to ensure $.map() will keep null values in the resulting array
			_initialState = $.map(observables, function(value) { return [value()]; });
			_initiallyDirty(initiallyDirty || false);
		};
	}
	
	function getFlashMessages(element) {
		if (!flashMessages) {
			flashMessages = new FlashMessagesViewModel();
			ko.applyBindings(flashMessages, element);
		}
		return flashMessages;
	}
	
	// Add those methods to ko namespaces
	if (!ko) ko = {};
	if (!ko.utils) ko.utils = {};
	if (!ko.errors) ko.errors = {};
	ko.utils.extract = extract;
	ko.utils.ajax = ajax;
	ko.utils.range = range;
	ko.utils.firstIndex = firstIndex;
	ko.utils.filterById = filterById;
	ko.utils.compareByString = compareByString;
	ko.utils.compareByNumber = compareByNumber;
	ko.utils.getFlashMessages = getFlashMessages;
	ko.utils.DirtyFlag = DirtyFlag;
	ko.errors.ErrorsViewModel = ErrorsViewModel;
})(typeof window === "undefined" ? this : window);
