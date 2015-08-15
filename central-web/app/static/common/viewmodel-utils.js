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
	
	function ErrorsViewModel(keys) {
		var self = this;

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
			console.log('ErrorsViewModel.reset');
			console.log(keyErrors);
			console.log(errors);
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
			console.log('xhr.status: ' + xhr.status);
			console.log('xhr.responseJSON: ');
			console.log(xhr.responseJSON);
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
	
	var viewModelHelpers = {
        	extract: extract,
        	ajax: ajax,
        	firstIndex: firstIndex,
        	filterById: filterById,
        	compareByString: compareByString,
        	ErrorsViewModel: ErrorsViewModel
	};
	
    /**
     * export to either browser or node.js
     */
    if (typeof exports !== "undefined") {
        exports.viewModelHelpers = viewModelHelpers;
    } else {
    	window.viewModelHelpers = viewModelHelpers;
        if (typeof define === "function" && define.amd) {
            define(function() {
                return {
                	viewModelHelpers: viewModelHelpers
                };
            });
        }
    }
})(typeof window === "undefined" ? this : window);
