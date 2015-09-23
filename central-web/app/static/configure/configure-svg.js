(function(window) {
	svg = {};
	var transformRequestObj;
	var transList;
	var dragTarget = null;
	var dragging = false;
	var offsetX = 0;
	var offsetY = 0;
	
	svg.deviceCoordinates = {};

	function getPoint(evt) {
		var pnt = dragTarget.ownerSVGElement.createSVGPoint();
		pnt.x = evt.clientX;
		pnt.y = evt.clientY;
		//---elements in different(svg) viewports, and/or transformed ---
		var sCTM = dragTarget.getScreenCTM();
		return pnt.matrixTransform(sCTM.inverse());
	}
	
	function startDrag(evt) {
		// Prevents dragging conflicts on other draggable elements
		if (!dragging) {
			dragTarget = evt.target;
	
			//---reference point to its respective viewport--
			var point = getPoint(evt);
			transformRequestObj = dragTarget.ownerSVGElement.createSVGTransform();
	
			//---attach new or existing transform to element, init its transform list---
			var myTransListAnim = dragTarget.transform;
			transList = myTransListAnim.baseVal;
	
			offsetX = point.x;
			offsetY = point.y;
	
			dragging = true;
		}
	}
	
	//---mouse move---
	function drag(evt) {
		if (dragging) {
			var point = getPoint(evt);
			point.x -= offsetX;
			point.y -= offsetY;
	
			transformRequestObj.setTranslate(point.x, point.y);
			transList.appendItem(transformRequestObj);
			transList.consolidate();
		}
	}
	
	//--mouse up---
	function endDrag(evt) {
		dragging = false;
	
		var point = getPoint(evt);
		point.x -= offsetX;
		point.y -= offsetY;
	
		transformRequestObj.setTranslate(point.x, point.y);
		transList.appendItem(transformRequestObj);
		matrix = transList.consolidate().matrix;
		
		// Apply transform matrix "manually" to circle center
		x = dragTarget.cx.baseVal.value;
		y = dragTarget.cy.baseVal.value;
		xx = matrix.a * x + matrix.c * y + matrix.e;
		yy = matrix.b * x + matrix.d * y + matrix.f;
		
		// Add this device to the list of devices changed
		svg.deviceCoordinates[dragTarget.getAttribute('data-uri')] = { 'x': xx, 'y': yy };
	}
	
	// Add those methods to svg namespace
	svg.startDrag = startDrag;
	svg.drag = drag;
	svg.endDrag = endDrag;
})(typeof window === "undefined" ? this : window);
