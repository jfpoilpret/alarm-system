#ifndef ACTIVATIONNETWORK_HH_
#define ACTIVATIONNETWORK_HH_

#include "NetworkUtils.hh"

// This class handles all communication with the alarm center, including ciphering
class ActivationTransmitter: public AbstractTransmitter
{
public:
	ActivationTransmitter(uint8_t server);

	// Send the newly typed code to the center and get updated state (locked/unlocked)
	LockStatus sendCodeAndGetLockStatus(const char* input, bool locking);
};

#endif /* ACTIVATIONNETWORK_HH_ */
