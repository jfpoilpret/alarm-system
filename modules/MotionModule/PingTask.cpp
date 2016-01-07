#include <Cosa/PinChangeInterrupt.hh>
#include "PingTask.hh"

PingTask::PingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter)
	:DefaultPingTask(clock, period, transmitter) {}

#ifndef BOARD_ATTINYX4
static OutputPin GREEN = Board::D19;	// UNO: A5
static OutputPin YELLOW = Board::D18;	// UNO: A4
static OutputPin RED = Board::D17;		// UNO: A3
#endif

void PingTask::status_changed(LockStatus status)
{
#ifndef BOARD_ATTINYX4
	GREEN.off();
	RED.off();
	YELLOW.off();
#endif
	switch (status)
	{
		case UNLOCKED:
#ifndef BOARD_ATTINYX4
		GREEN.on();
#endif
		PinChangeInterrupt::end();
		break;
		
		case LOCKED:
#ifndef BOARD_ATTINYX4
		RED.on();
#endif
		PinChangeInterrupt::begin();
		break;
		
		case UNKNOWN:
#ifndef BOARD_ATTINYX4
		YELLOW.on();
#endif
		break;
	}
}
