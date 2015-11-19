/* 
 * File:   Handlers.cpp
 */

#include <fstream>
#include "RFManager.h"

DevicesHandler& Handler::handler() const {
	return *handler_;
}

AlarmStatus& Handler::status() const {
	return handler_->status;
}

NRF24L01P& Handler::nrf() const {
	return handler_->nrf;
}

double Handler::cipher_duration() const {
	return handler_->cipher_duration;
}

Device* Handler::device(const uint8_t id) const {
	if (handler_->ciphered_devices.count(id))
		return &handler_->ciphered_devices[id];
	else
		return 0;
}

std::string Handler::code() const {
	return handler_->code;
}

time_t Handler::now() const {
	time_t current;
	time(&current);
	return current;
}

const MessageType PingHandler::PORT = MessageType::PING_SERVER;
std::string PingHandler::execute(uint8_t id, MessageType port, ReceptionPayload& payload) {
	std::ostringstream output;
	output << (uint16_t) id << ' ' << now() << " PING";
	Device* dev = device(id);
	if (dev and difftime(now(), dev->creation_time) > cipher_duration()) {
		// Generate new cipher key and send back
		uint8_t sent_payload[XTEA::KEY_SIZE + 1];
		sent_payload[0] = status().locked;
		XTEA::generate_key(&sent_payload[1]);
		// Always ensure send is successful before updating cipher locally
		if (nrf().send(id, static_cast<uint8_t>(port), sent_payload, sizeof sent_payload) > 0) {
			dev->cipher.set_key(&sent_payload[1]);
			dev->creation_time = now();
		} else {
			std::cerr << "Cipher update failed: " << std::endl; 
		}
	} else {
		// Simply return lock
		nrf().send(id, static_cast<uint8_t>(port), &status().locked, sizeof status().locked);
	}
	return output.str();
}

const MessageType VoltageHandler::PORT = MessageType::VOLTAGE_LEVEL;
std::string VoltageHandler::execute(uint8_t id, MessageType port, ReceptionPayload& payload) {
	std::ostringstream output;
	output << (uint16_t) id << ' ' << now() << " VOLT " << payload.voltage;
	return output.str();
}

const MessageType LockHandler::PORT1 = MessageType::LOCK_CODE;
const MessageType LockHandler::PORT2 = MessageType::UNLOCK_CODE;
std::string LockHandler::execute(uint8_t id, MessageType port, ReceptionPayload& payload) {
	std::ostringstream output;
	device(id)->cipher.decipher(payload.crypted_code);
	if (code() == payload.code)
		status().locked = (port == MessageType::LOCK_CODE);
	nrf().send(id, static_cast<uint8_t>(port), &status().locked, sizeof status().locked);
	output << (uint16_t) id << ' ' << now() << (port == MessageType::LOCK_CODE ? " LOCK " : " UNLOCK ") << payload.code;
	return output.str();
}
