#include "MotionNetwork.hh"
#include "Pins.hh"

ActivationTransmitter::ActivationTransmitter(uint16_t network, uint8_t device, uint8_t server)
	:AbstractTransmitter(network, device, server, RF_CSN, RF_CE, RF_IRQ) {}

LockStatus ActivationTransmitter::sendCodeAndGetLockStatus(const char* input, bool locking)
{
	auto_standby standby(*this);
	// Send lock/unlock code to server
	char buffer[8];
	strcpy(buffer, input);
	_cipher.encipher((uint32_t*) buffer);
	if (send(_server, (locking ? LOCK_CODE : UNLOCK_CODE), buffer, sizeof(buffer)) < 0)
		// If server is down, we consider that the lock status did not change
		return UNKNOWN;
	// Wait for acknowledge with lock status
	uint8_t source;
	uint8_t port;
	bool lock;
	if (recv(source, port, &lock, sizeof(lock), RECV_TIMEOUT_MS) < 0)
		// If problem receiving server response, we consider that system is unlocked
		return UNKNOWN;
	if (source == _server && port == (locking ? LOCK_CODE : UNLOCK_CODE))
		return lock ? LOCKED : UNLOCKED;
	// We received a wrong message what do we do with it?
	// We consider that the lock status did not change
	return UNKNOWN;
}
