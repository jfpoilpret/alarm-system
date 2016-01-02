/* 
 * File:   Handlers.h
 */

#ifndef HANDLERS_H
#define	HANDLERS_H

#include <ctime>
#include <string>
#include "Cipher.h"
#include "NRF24L01P.h"
#include "RFManager.h"

class DevicesHandler;

struct Device {
	XTEA cipher;
	time_t creation_time;
};
	
enum class MessageType: uint8_t {
	// General messages, used by all sensors
	PING_SERVER = 0x01,
	VOLTAGE_LEVEL = 0x02,

	// Messages specific to the activation module
	LOCK_CODE = 0x10,
	UNLOCK_CODE = 0x11,

	// Messages specific to the motion detection module
	MOTION_DETECTED = 0x20
			
	// Other messages will go there
};

const size_t MESSAGE_MAX_SIZE = NRF24L01P::PAYLOAD_MAX;

#pragma pack(1)
union ReceptionPayload {
	uint8_t raw[MESSAGE_MAX_SIZE];
	uint32_t crypted_code[2];
	char code[8];
	uint16_t voltage;
};
#pragma pack()

class Handler {
public:
	virtual std::string execute(uint8_t id, MessageType port, ReceptionPayload& payload) = 0;
	
protected:
	DevicesHandler& handler() const;
	AlarmStatus& status() const;
	NRF24L01P& nrf() const;
	double cipher_duration() const;
	Device* device(const uint8_t id) const;
	std::string code() const;
	time_t now() const;

private:
	DevicesHandler* handler_;
	friend class DevicesHandler;
};

class PingHandler: public Handler {
public:
	static const MessageType PORT;
	virtual std::string execute(uint8_t id, MessageType port, ReceptionPayload& payload);
};

class VoltageHandler: public Handler {
public:
	static const MessageType PORT;
	virtual std::string execute(uint8_t id, MessageType port, ReceptionPayload& payload);
};

class LockHandler: public Handler {
public:
	static const MessageType PORT1;
	static const MessageType PORT2;
	virtual std::string execute(uint8_t id, MessageType port, ReceptionPayload& payload);
};

class MotionHandler: public Handler {
public:
	static const MessageType PORT;
	virtual std::string execute(uint8_t id, MessageType port, ReceptionPayload& payload);
};

#endif	/* HANDLERS_H */
