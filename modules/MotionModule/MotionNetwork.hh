#ifndef ACTIVATIONNETWORK_HH_
#define ACTIVATIONNETWORK_HH_

#include "NetworkUtils.hh"

// This class handles all communication with the alarm center, including ciphering
class MotionTransmitter: public AbstractTransmitter
{
public:
	MotionTransmitter(uint16_t network, uint8_t device, uint8_t server);

};

#endif /* ACTIVATIONNETWORK_HH_ */
