/* 
 * File:   CommandManager.cpp
 */

#include "RFManager.h"

const size_t MESSAGE_MAX_SIZE = NRF24L01P::PAYLOAD_MAX;

#pragma pack(1)
union ReceptionPayload {
	uint8_t raw[MESSAGE_MAX_SIZE];
	uint32_t crypted_code[2];
	char code[8];
	uint16_t voltage;
};
#pragma pack()

//TODO Conversion map of port -> string (data pipe)

DevicesHandler::DevicesHandler(zmq::context_t& context, AlarmStatus& status)
:	data(context, ZMQ_PUB), 
	status(status), 
	cipher_duration(0.0),
	nrf(0, 0) {
	// Initialize socket
	data.bind("ipc:///tmp/alarm-system/devices.ipc");
}

DevicesHandler::~DevicesHandler() {
	// Ensure thread is stopped first
	stop();
	data.close();
}

void DevicesHandler::set_address(uint16_t network, uint8_t server) {
	nrf.set_address(network, server);
}

void DevicesHandler::set_cipher_duration(double seconds) {
	cipher_duration = seconds;
}

void DevicesHandler::set_ciphered_devices(uint16_t count, const uint8_t* device_ids) {
	ciphered_devices.clear();
	for (uint16_t i = 0; i < count; ++i) {
		Device device;
		device.creation_time = 0;
		ciphered_devices[device_ids[i]] = device;
	}
}

void DevicesHandler::start() {
	stop();
	status.active = true;
	thread = std::thread(&DevicesHandler::run, this);
}

void DevicesHandler::stop() {
	if (status.active) {
		// Signal thread to interrupt
		status.active = false;
		if (thread.joinable()) thread.join();
	}
}

void DevicesHandler::run() {
	// Infinite loop waiting for devices messages
	nrf.begin();
	while (status.active) {
		// Wait for receiving a device message
		uint8_t device;
		uint8_t port;
		ReceptionPayload msg;
		int count = nrf.recv(device, port, msg.raw, sizeof msg, 1000L);
		if (count >= 0) {
			time_t now;
			time(&now);
			std::ostringstream output;
			output << (uint16_t) device << ' ' << now << ' ';
			//TODO handle message (redesign later to use a map<port, functor>)
			switch (port) {
				case PING_SERVER:
					if (	ciphered_devices.count(device)
						&&	difftime(ciphered_devices[device].creation_time, now) > cipher_duration) {
						// Generate new cipher key and send back
						uint8_t payload[XTEA::KEY_SIZE + 1];
						payload[0] = status.locked;
						XTEA::generate_key(&payload[1]);
						// Always ensure send is successful before updating cipher locally
						if (nrf.send(device, port, payload, sizeof payload) > 0) {
							ciphered_devices[device].cipher.set_key(&payload[1]);
							ciphered_devices[device].creation_time = now;
						}
					} else {
						// Simply return lock
						nrf.send(device, port, &status.locked, sizeof status.locked);
					}
					output << "PING";
					break;
					
				case VOLTAGE_LEVEL:
					output << "VOLT " << msg.voltage;
					break;
					
				case LOCK_CODE:
				case UNLOCK_CODE:
					nrf.send(device, port, &status.locked, sizeof status.locked);
					ciphered_devices[device].cipher.decipher(msg.crypted_code);
					output << (port == LOCK_CODE ? "LOCK " : "UNLOCK ") << msg.code;
					break;
			}
			s_send(data, output.str());
		}
	}
	nrf.end();
}

CommandManager::CommandManager(zmq::context_t& context, AlarmStatus& status)
:	command(context, ZMQ_REP), 
	handler(context, status), 
	status(status) {
	// Initialize socket
	command.bind("ipc:///tmp/alarm-system/command.ipc");
	// Initialize thread blocked on receiving commands
	thread = std::thread(&CommandManager::run, this);
}

CommandManager::~CommandManager() {
	command.close();
}

void CommandManager::block_until_exit() {
	// Wait until command reception naturally terminates i.e. when receiving EXIT command
	thread.join();
}

void CommandManager::run() {
	// Infinite loop waiting for commands (threaded)
	while (true) {
		std::string cmd = s_recv(command);
		std::istringstream input(cmd);
		std::string verb;
		input >> verb;
		std::string result = "OK";
		
		// Check command and dispatch where needed
		if (verb == "START")
			handler.start();
		else if (verb == "STOP" or verb == "EXIT")
			handler.stop();
		else if (verb == "LOCK")
			status.locked = true;
		else if (verb == "UNLOCK")
			status.locked = false;
		else if (verb == "INIT") {
			// Parse INIT argumensts: network server_id cipher_delay cipher_dev_id1 cipher_dev_id2...
			// All integer ar expected in hexa format
			// cipher_delay is a double in seconds
			uint16_t network;
			uint16_t server;
			double duration;
			input >> std::hex >> network >> server >> duration;
			handler.set_address(network, server);
			handler.set_cipher_duration(duration);
			std::cout << "INIT " << std::hex << network << " " << server << " " << duration << std::endl;
			std::vector<uint8_t> devices;
			while (!input.eof()) {
				uint16_t id;
				input >> id;
				devices.push_back(id);
			}
			handler.set_ciphered_devices(devices.size(), devices.data());
		} else
			result = "INVALID COMMAND";
		s_send(command, result);
		if (verb == "EXIT")
			break;
	}
}
