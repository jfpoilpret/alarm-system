#include "MotionNetwork.hh"
#include "MotionDetector.hh"
#include "Pins.hh"

MotionTransmitter::MotionTransmitter(uint8_t server)
	:AbstractTransmitter(server, RF_CSN, RF_CE, RF_IRQ), Handler() {}

#ifndef BOARD_ATTINYX4
static OutputPin YELLOW = Board::D18;
#endif

void MotionTransmitter::on_event(uint8_t type, uint16_t value)
{
	UNUSED(value);
	UNUSED(type);
#ifndef BOARD_ATTINYX4
	//DEBUG to YELLOW LED (A4)
	YELLOW.toggle();
#endif
	auto_standby standby(*this);
	send(_server, MOTION_DETECTED, 0, 0);
}
