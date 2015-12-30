#ifndef ACTIVATIONNETWORK_HH_
#define ACTIVATIONNETWORK_HH_

#include <Cosa/Event.hh>
#include "NetworkUtils.hh"

// This class handles all communication with the alarm center, including ciphering
class MotionTransmitter: public AbstractTransmitter, public Event::Handler
{
public:
	MotionTransmitter(uint8_t server);
	virtual void on_event(uint8_t type, uint16_t value);
};

#endif /* ACTIVATIONNETWORK_HH_ */
