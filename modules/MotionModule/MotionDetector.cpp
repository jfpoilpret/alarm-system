#include "MotionDetector.hh"
#include "Pins.hh"

void MotionDetector::on_interrupt(uint16_t arg)
{
	UNUSED(arg);
	Event::push(MOTION_EVENT, _handler, this);
}
