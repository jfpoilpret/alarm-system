#include "MotionDetector.hh"
#include "Pins.hh"

MotionDetector::MotionDetector(Event::Handler* handler)
	:PinChangeInterrupt(PIR_OUTPUT, PinChangeInterrupt::ON_RISING_MODE), _handler(handler)
{
	//FIXME should not enable until Transmitter is started!
	enable();
}

void MotionDetector::on_interrupt(uint16_t arg)
{
	UNUSED(arg);
	Event::push(MOTION_EVENT, _handler, this);
}
