#include "MotionNetwork.hh"
#include "Pins.hh"

MotionTransmitter::MotionTransmitter(uint16_t network, uint8_t device, uint8_t server)
	:AbstractTransmitter(network, device, server, RF_CSN, RF_CE, RF_IRQ) {}

