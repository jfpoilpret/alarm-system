
var TransformRequestObj;
var TransList;
var DragTarget = null;
var Dragging = false;
var OffsetX = 0;
var OffsetY = 0;

//---mouse down over element---
function startDrag(evt)
{
	if(!Dragging) //---prevents dragging conflicts on other draggable elements---
	{
		DragTarget = evt.target;

		//---reference point to its respective viewport--
		var pnt = DragTarget.ownerSVGElement.createSVGPoint();
		pnt.x = evt.clientX;
		pnt.y = evt.clientY;

		var sCTM = DragTarget.getScreenCTM();
		var Pnt = pnt.matrixTransform(sCTM.inverse());

		TransformRequestObj = DragTarget.ownerSVGElement.createSVGTransform();

		//---attach new or existing transform to element, init its transform list---
		var myTransListAnim = DragTarget.transform;
		TransList = myTransListAnim.baseVal;

		OffsetX = Pnt.x;
		OffsetY = Pnt.y;

		Dragging = true;
	}
}

//---mouse move---
function drag(evt)
{
	if(Dragging)
	{
		var pnt = DragTarget.ownerSVGElement.createSVGPoint();
		pnt.x = evt.clientX;
		pnt.y = evt.clientY;
		//---elements in different(svg) viewports, and/or transformed ---
		var sCTM = DragTarget.getScreenCTM();
		var Pnt = pnt.matrixTransform(sCTM.inverse());
		Pnt.x -= OffsetX;
		Pnt.y -= OffsetY;

		TransformRequestObj.setTranslate(Pnt.x,Pnt.y);
		TransList.appendItem(TransformRequestObj);
		TransList.consolidate();
	}
}

//--mouse up---
function endDrag(evt)
{
	Dragging = false;

	var pnt = DragTarget.ownerSVGElement.createSVGPoint();
	pnt.x = evt.clientX;
	pnt.y = evt.clientY;

	var sCTM = DragTarget.getScreenCTM();
	var Pnt = pnt.matrixTransform(sCTM.inverse());
	Pnt.x -= OffsetX;
	Pnt.y -= OffsetY;

	TransformRequestObj.setTranslate(Pnt.x, Pnt.y);
	TransList.appendItem(TransformRequestObj);
	TransList.consolidate();
}
