#include "MotionDetector.hh"
#include "Pins.hh"

MotionDetector::MotionDetector(Event::Handler* handler)
	:PinChangeInterrupt(PIR_OUTPUT, PinChangeInterrupt::ON_RISING_MODE), _handler(handler) {}

#ifndef BOARD_ATTINYX4
static OutputPin GREEN = Board::D19;
#endif

void MotionDetector::on_interrupt(uint16_t arg)
{
	UNUSED(arg);
#ifndef BOARD_ATTINYX4
	//DEBUG to GREEN LED (A5))
	GREEN.toggle();
#endif
	Event::push(MOTION_EVENT, _handler, this);
}
