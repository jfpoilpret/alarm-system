#include "PingTask.hh"

//PingTask::PingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter, PinChangeInterrupt& detector)
PingTask::PingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter, MotionDetector& detector)
	:DefaultPingTask(clock, period, transmitter), _detector(detector) {}

#ifndef BOARD_ATTINYX4
static OutputPin GREEN = Board::D19;	// UNO: A5
static OutputPin YELLOW = Board::D18;	// UNO: A4
static OutputPin RED = Board::D17;		// UNO: A3
#endif

void PingTask::status(LockStatus status)
{
#ifndef BOARD_ATTINYX4
	GREEN.off();
	RED.off();
	YELLOW.off();
#endif
	// It seems status is never UNLOCKED; add some debug LEDs here...)
	switch (status)
	{
		case UNLOCKED:
#ifndef BOARD_ATTINYX4
		GREEN.on();
#endif
		PinChangeInterrupt::end();
//		_detector.disable();
		break;
		
		case LOCKED:
#ifndef BOARD_ATTINYX4
		RED.on();
#endif
		PinChangeInterrupt::begin();
//		_detector.enable();
		break;
		
		case UNKNOWN:
#ifndef BOARD_ATTINYX4
		YELLOW.on();
#endif
		break;
	}
}
