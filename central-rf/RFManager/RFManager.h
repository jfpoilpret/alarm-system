/* 
 * File:   CommandManager.h
 */

#ifndef RFMANAGER_H
#define	RFMANAGER_H

#include <ctime>
#include <map>
#include <thread>
#include "Cipher.h"
#include "NRF24L01P.h"
#include "zhelpers.hpp"

struct AlarmStatus {
	bool active;
	bool locked;
	
	AlarmStatus():active(false), locked(false) {}
};

// Devices Handler: handles NRF24 communication to devices and pushes messages to Python Alarm System
class DevicesHandler {
public:
	DevicesHandler(zmq::context_t& context, AlarmStatus& status);
	~DevicesHandler();
	DevicesHandler(const DevicesHandler&) = delete;
	
	void set_address(uint16_t network, uint8_t server);
	void set_cipher_duration(double seconds);
	void set_ciphered_devices(uint16_t count, const uint8_t* device_ids);
	void start();
	void stop();
	
private:
	void run();
	
	struct Device {
		XTEA cipher;
		time_t creation_time;
	};
	
	enum MessageType {
		// General messages, used by all sensors
		PING_SERVER = 0x01,
		VOLTAGE_LEVEL = 0x02,

		// Messages specific to the activation module
		LOCK_CODE = 0x10,
		UNLOCK_CODE = 0x11,

		// Other messages will go there
	};
	
	zmq::socket_t data;
	AlarmStatus& status;
	double cipher_duration;
	std::map<uint8_t, Device> ciphered_devices;
	std::thread thread;
	NRF24L01P nrf;
};

// Command Manager: receives commands from Python Alarm System, interprets and dispatch them
class CommandManager {
public:
	CommandManager(zmq::context_t& context, AlarmStatus& status);
	CommandManager(const CommandManager&) = delete;
	~CommandManager();
	
	void block_until_exit();

private:
	void run();

	zmq::socket_t command;
	DevicesHandler handler;
	AlarmStatus& status;
	std::thread thread;
};

#endif	/* RFMANAGER_H */

