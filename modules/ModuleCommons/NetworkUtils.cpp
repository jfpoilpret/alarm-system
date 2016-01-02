#include "NetworkUtils.hh"
#include "RTTUtils.hh"

auto_standby::auto_standby(AbstractTransmitter& transmitter) : _rf(transmitter._nrf) {}

AbstractTransmitter::AbstractTransmitter(uint8_t server, 
	Board::DigitalPin csn, Board::DigitalPin ce, Board::ExternalInterruptPin irq)
	:_nrf(0, 0, csn, ce, irq), _server(server) {}

void AbstractTransmitter::begin(int16_t net, uint8_t dev)
{
	_nrf.address(net, dev);
	_nrf.begin();
//		set_output_power_level(-18);
}

int AbstractTransmitter::recv(uint8_t& src, uint8_t& port, void* buf, size_t count, uint32_t ms)
{
	auto_RTT rtc;
	return _nrf.recv(src, port, buf, count, ms);
}

int AbstractTransmitter::send(uint8_t dest, uint8_t port, const void* buf, size_t len)
{
	return _nrf.send(dest, port, buf, len);
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
