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

DevicesHandler::DevicesHandler(zmq::context_t& context, AlarmStatus& status)
:	data(context, ZMQ_PUB), 
	status(status), 
	cipher_duration(0.0),
	code(),
	nrf(0, 0),
	port_handlers() {
	// Initialize socket
	data.bind("ipc:///tmp/alarm-system/devices.ipc");
}

DevicesHandler::~DevicesHandler() {
	// Ensure thread is stopped first
	stop();
	data.close();
}

void DevicesHandler::add_handler(const MessageType port, Handler* handler) {
	handler->handler_ = this;
	port_handlers[static_cast<uint8_t>(port)] = handler;
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

void DevicesHandler::get_status(uint16_t& trans, uint16_t& retrans, uint16_t& drops, uint16_t& missing_irqs) const {
	trans = nrf.get_trans();
	retrans = nrf.get_retrans();
	drops = nrf.get_drops();
	missing_irqs = nrf.get_missing_irq();
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
			if (port_handlers.count(port) > 0) {
				s_send(data, port_handlers[port]->execute(device, static_cast<MessageType>(port), msg));
			} else {
				// log error
				std::cerr << "Received unknown port " << std::hex << port << " from device " << device << std::endl;
			}
		}
	}
	nrf.end();
}

CommandManager::CommandManager(zmq::context_t& context, DevicesHandler& handler, AlarmStatus& status)
:	command(context, ZMQ_REP), 
	handler(handler), 
	status(status),
	running(false),
	command_handlers() {
	// Initialize socket
	command.bind("ipc:///tmp/alarm-system/command.ipc");
}

CommandManager::~CommandManager() {
	command.close();
	// Normal termination: remove INIT commands storage
	Command::remove(InitCommand::VERB);
	Command::remove(CodeCommand::VERB);
	Command::remove(LockCommand::VERB);
	Command::remove(StartCommand::VERB);
}

void CommandManager::start() {
	// Initialize status from last saved log (only if previous run was abnormally terminated)
	execute(InitCommand::VERB);
	execute(CodeCommand::VERB);
	execute(LockCommand::VERB);
	execute(StartCommand::VERB);
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
	auto command = command_handlers.find(verb);
	if (command != command_handlers.end()) {
		command->second->log =log;
		return command->second->execute(verb, input);
	}
	return "INVALID COMMAND";
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
		std::ifstream init(file);
		while (true) {
			std::string line;
			std::getline(init, line);
			if (init.eof()) break;
			if (init.fail() or init.bad()) {
				std::cerr << "Error reading file `" << file << "`" << std::endl;
				break;
			}
			std::istringstream input(line);
			std::string verb2;
			input >> verb2;
			handle_command(verb2, input, false);
		}
		init.close();
	}
}

