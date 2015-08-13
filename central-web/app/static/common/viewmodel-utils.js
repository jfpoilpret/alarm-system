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
	
    /**
     * export to either browser or node.js
     */
    if (typeof exports !== "undefined") {
        exports.extract = extract
        exports.ajax = ajax
        exports.firstIndex = firstIndex
        exports.filterById = filterById
        exports.compareByString = compareByString
    } else {
    	window.extract = extract
    	window.ajax = ajax
    	window.firstIndex = firstIndex
    	window.filterById = filterById
    	window.compareByString = compareByString

        if (typeof define === "function" && define.amd) {
            define(function() {
                return {
                	extract: extract,
                	ajax: ajax,
                	firstIndex: firstIndex,
                	filterById: filterById,
                	compareByString: compareByString
                }
            })
        }
    }
})(typeof window === "undefined" ? this : window);
