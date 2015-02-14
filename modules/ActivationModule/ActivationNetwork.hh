/*
 * ActivationNetwork.hh
 *
 *  Created on: 19 janv. 2015
 *      Author: Jean-François
 */

#ifndef ACTIVATIONNETWORK_HH_
#define ACTIVATIONNETWORK_HH_

#include <Cosa/Wireless/Driver/NRF24L01P.hh>

#include "Cipher.hh"
#include "RTCAdapter.hh"
#include "Pins.hh"

//TODO isolate all Message Types, Devices IDs... in a specific header, shared among all projects
enum MessageType
{
	// General messages, used by all sensors
	PING_SERVER = 0x01,
	VOLTAGE_LEVEL = 0x02,

	// Messages specific to the activation module
	LOCK_CODE = 0x10,
	UNLOCK_CODE = 0x11,

	// Other messages will go there

} __attribute__((packed));

struct RxPingServer
{
	bool locked;
	uint8_t key[XTEA::KEY_SIZE];
};

union RxPayload
{
	RxPingServer pingServer;
};

//FIXME system fails completely when server is down...
// This class handles all communication with the alarm center, including ciphering
class ActivationTransmitter: public NRF24L01P
{
public:
	ActivationTransmitter(uint16_t network, uint8_t device, uint8_t server)
		:	NRF24L01P(network, device, RF_CSN, RF_CE, RF_IRQ),
		 	_server(server)
	{
		begin();
//		set_output_power_level(-18);
	}

	//TODO improve return type: use enum with more possibilities (to handle error cases)
	// Register the activation module to the alarm center, get new cipher key,
	// get current alarm status (locked/unlocked).
	// Normally this method is called every 5 seconds.
	bool pingServerAndGetLockStatus();
	// Send the newly typed code to the center and get updated state (locked/unlocked)
	bool sendCodeAndGetLockStatus(const char* input, bool locking);
	// Notify alarm center about current voltage level (in mV).
	// This method is typically called once per hour or so
	void sendVoltageLevel(uint16_t level);

private:
	virtual int recv(uint8_t& src, uint8_t& port, void* buf, size_t count, uint32_t ms = 0L);

	class auto_standby
	{
	public:
		auto_standby(ActivationTransmitter& rf):_rf(rf) {}
		~auto_standby() { _rf.standby(); }
	private:
		ActivationTransmitter& _rf;
	};

	static const uint8_t RECV_TIMEOUT_MS = 5;
	const uint8_t _server;
	XTEA _cipher;
};

int ActivationTransmitter::recv(uint8_t& src, uint8_t& port, void* buf, size_t count, uint32_t ms)
{
	if (ms == 0)
		return NRF24L01P::recv(src, port, buf, count, ms);
	RTCAdapter();
	return NRF24L01P::recv(src, port, buf, count, ms);
}

bool ActivationTransmitter::pingServerAndGetLockStatus()
{
	auto_standby(*this);
	// Ping server
	if (send(_server, PING_SERVER, 0, 0) < 0)
		// If server is down, we consider that system is unlocked
		return false;
	// Wait for acknowledge with lock status and optional cipher key
	uint8_t source;
	uint8_t port;
	RxPingServer response;
	int size = recv(source, port, &response, sizeof(response), RECV_TIMEOUT_MS);
	if (size <= 0)
		// If problem receiving server response, we consider that system is unlocked
		return false;
	if (source == _server && port == PING_SERVER)
	{
		if ((unsigned) size >= sizeof(response))
			// Update key
			_cipher.set_key(response.key);
		return response.locked;
	}
	// We received a wrong message what do we do with it?
	// For the moment just consider the system should be considered locked
	return true;
}

bool ActivationTransmitter::sendCodeAndGetLockStatus(const char* input, bool locking)
{
	auto_standby(*this);
	// Send lock/unlock code to server
	char buffer[8];
	strcpy(buffer, input);
	_cipher.encipher((uint32_t*) buffer);
	if (send(_server, (locking ? LOCK_CODE : UNLOCK_CODE), buffer, sizeof(buffer)) < 0)
		// If server is down, we consider that the lock status did not change
		return !locking;
	// Wait for acknowledge with lock status
	uint8_t source;
	uint8_t port;
	bool lock;
	if (recv(source, port, &lock, sizeof(lock), RECV_TIMEOUT_MS) < 0)
		// If problem receiving server response, we consider that system is unlocked
		return false;
	if (source == _server && port == (locking ? LOCK_CODE : UNLOCK_CODE))
		return lock;
	// We received a wrong message what do we do with it?
	// We consider that the lock status did not change
	return !locking;
}

void ActivationTransmitter::sendVoltageLevel(uint16_t level)
{
	auto_standby(*this);
	send(_server, VOLTAGE_LEVEL, &level, sizeof(level));
}

#endif /* ACTIVATIONNETWORK_HH_ */
