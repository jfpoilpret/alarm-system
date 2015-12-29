#include "NetworkUtils.hh"
#include "RTTUtils.hh"

AbstractTransmitter::AbstractTransmitter(uint16_t network, uint8_t device, uint8_t server, 
	Board::DigitalPin csn, Board::DigitalPin ce, Board::ExternalInterruptPin irq)
	:	NRF24L01P(network, device, csn, ce, irq), _server(server)
{
	begin();
//		set_output_power_level(-18);
}

int AbstractTransmitter::recv(uint8_t& src, uint8_t& port, void* buf, size_t count, uint32_t ms)
{
	auto_RTT rtc;
	return NRF24L01P::recv(src, port, buf, count, ms);
}

LockStatus AbstractTransmitter::pingServerAndGetLockStatus()
{
	auto_standby standby(*this);
	// Ping server
	if (send(_server, PING_SERVER, 0, 0) < 0)
		// If server is down, we consider that system is unlocked
		return UNKNOWN;
	// Wait for acknowledge with lock status and optional cipher key
	uint8_t source;
	uint8_t port;
	RxPingServer response;
	int size = recv(source, port, &response, sizeof(response), RECV_TIMEOUT_MS);
	if (size <= 0)
		// If problem receiving server response, we consider that system is unlocked
		return UNKNOWN;
	if (source == _server && port == PING_SERVER)
	{
#ifndef NO_CIPHER
		if ((unsigned) size >= sizeof(response))
			// Update key
			_cipher.set_key(response.key);
#endif
		return response.locked ? LOCKED : UNLOCKED;
	}
	// We received a wrong message what do we do with it?
	// For the moment just consider the system should be considered locked
	return UNKNOWN;
}

void AbstractTransmitter::sendVoltageLevel(uint16_t level)
{
	auto_standby standby(*this);
	send(_server, VOLTAGE_LEVEL, &level, sizeof(level));
}
