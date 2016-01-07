#include "MotionNetwork.hh"
#include "MotionDetector.hh"
#include "Pins.hh"

MotionTransmitter::MotionTransmitter(uint8_t server)
	:AbstractTransmitter(server, RF_CSN, RF_CE, RF_IRQ), Handler() {}

void MotionTransmitter::on_event(uint8_t type, uint16_t value)
{
	UNUSED(value);
	UNUSED(type);
	auto_standby standby(*this);
	send(_server, MOTION_DETECTED, 0, 0);
}
