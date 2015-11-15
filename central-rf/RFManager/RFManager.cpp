/* 
 * File:   CommandManager.cpp
 */

#include <time.h>
#include <sys/stat.h>
#include <fstream>
#include <stdexcept>
#include "RFManager.h"

static timespec current_time() {
	timespec time;
	clock_gettime(CLOCK_REALTIME, &time);
	return time;
}

static uint64_t us_since(const timespec& since) {
	timespec now = current_time();
	return (now.tv_sec - since.tv_sec) * 1000000 + (now.tv_nsec - since.tv_nsec) / 1000;
}

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
	code(),
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

void DevicesHandler::set_code(const std::string& code) {
	this->code = code;
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
			//TODO measure time to complete handling (most of it is spent in nrf.send())
			std::ostringstream output;
			output << (uint16_t) device << ' ' << now << ' ';
			//TODO handle message (redesign later to use a map<port, functor>)
			switch (port) {
				case PING_SERVER:
					if (	ciphered_devices.count(device)
						&&	difftime(now, ciphered_devices[device].creation_time) > cipher_duration) {
						// Generate new cipher key and send back
						uint8_t payload[XTEA::KEY_SIZE + 1];
						payload[0] = status.locked;
						XTEA::generate_key(&payload[1]);
						// Always ensure send is successful before updating cipher locally
						if (nrf.send(device, port, payload, sizeof payload) > 0) {
							ciphered_devices[device].cipher.set_key(&payload[1]);
							ciphered_devices[device].creation_time = now;
						} else {
							std::cerr << "Cipher update failed: " << std::endl; 
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
					ciphered_devices[device].cipher.decipher(msg.crypted_code);
					if (code == msg.code)
						status.locked = (port == LOCK_CODE);
					nrf.send(device, port, &status.locked, sizeof status.locked);
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
	status(status),
	running(false),
	command_handlers() {
	// Initialize socket
	command.bind("ipc:///tmp/alarm-system/command.ipc");
	// Initialize status from last saved log (only if previous run was abnormally terminated)
	//TODO should use Command::VERB here instead of constants
	execute("INIT");
	execute("CODE");
	execute("LOCK");
	execute("START");
}

CommandManager::~CommandManager() {
	command.close();
	// Normal termination: remove INIT commands storage
	remove("rfmanager.ini");
}

void CommandManager::start() {
	// Initialize thread blocked on receiving commands
	running = true;
	thread = std::thread(&CommandManager::run, this);
}

void CommandManager::exit() {
	running = false;
}

void CommandManager::block_until_exit() {
	// Wait until command reception naturally terminates i.e. when receiving EXIT command
	thread.join();
}

void CommandManager::add_command(const std::string& verb, Command* command) {
	command->manager = this;
	command_handlers[verb] = command;
}

std::string CommandManager::handle_command(const std::string& verb, std::istringstream& input, bool log) {
	// Check command and dispatch where needed
	try {
		Command* command = command_handlers[verb];
		command->log = log;
		return command->execute(verb, input);
	} catch (std::out_of_range e) {
		return "INVALID COMMAND";
	}
}

void CommandManager::run() {
	// Infinite loop waiting for commands (threaded)
	while (running) {
		std::string cmd = s_recv(command);
		std::istringstream input(cmd);
		std::string verb;
		input >> verb;
		std::string result = handle_command(verb, input, true);
		s_send(command, result);
	}
}

void CommandManager::execute(const std::string& verb) {
	std::string file = "rfmanager." + verb;
	struct stat sb;
	if (!stat(file.c_str(), &sb)) {
		std::string line;
		std::ifstream init(file);
		while (std::getline(init, line)) {
			std::istringstream input(line);
			std::string verb;
			input >> verb;
			handle_command(verb, input, false);
		}
		init.close();
	}
}

void Command::write(const std::string& verb, std::istringstream& input) {
	if (log) {
		std::string file = "rfmanager." + verb;
		std::ofstream output(file, std::ofstream::trunc);
		output << input.str() << std::endl;
		output.close();
	}
}

void Command::remove(const std::string& verb) {
	std::string file = "rfmanager." + verb;
	::remove(file.c_str());
}
