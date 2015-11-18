/* 
 * File:   Commands.cpp
 */

#include "Commands.h"
#include "RFManager.h"

DevicesHandler& Command::handler() const {
	return manager->handler;
}
AlarmStatus& Command::status() const {
	return manager->status;
}
void Command::exit() {
	manager->exit();
}

const char* InitCommand::VERB = "INIT";
std::string InitCommand::execute(const std::string& verb, std::istringstream& input) {
	write(InitCommand::VERB, input);
	// Parse INIT argumensts: network server_id cipher_delay cipher_dev_id1 cipher_dev_id2...
	// All integer ar expected in hexa format
	// cipher_delay is a double in seconds
	uint16_t network;
	uint16_t server;
	double duration;
	input >> std::hex >> network >> server >> duration;
	handler().set_address(network, server);
	handler().set_cipher_duration(duration);
	std::vector<uint8_t> devices;
	while (!input.eof()) {
		uint16_t id;
		input >> id;
		devices.push_back(id);
	}
	handler().set_ciphered_devices(devices.size(), devices.data());
	return "OK";
}

const char* CodeCommand::VERB = "CODE";
std::string CodeCommand::execute(const std::string& verb, std::istringstream& input) {
	write(CodeCommand::VERB, input);
	std::string code;
	input >> code;
	handler().set_code(code);
	return "OK";
}

const char* StartCommand::VERB = "START";
std::string StartCommand::execute(const std::string& verb, std::istringstream& input) {
	write(StartCommand::VERB, input);
	handler().start();
	return "OK";
}

const char* StopCommand::VERB = "STOP";
std::string StopCommand::execute(const std::string& verb, std::istringstream& input) {
	remove(StartCommand::VERB);
	handler().stop();
	return "OK";
}

const char* ExitCommand::VERB = "EXIT";
std::string ExitCommand::execute(const std::string& verb, std::istringstream& input) {
	remove(InitCommand::VERB);
	remove(CodeCommand::VERB);
	remove(StartCommand::VERB);
	handler().stop();
	exit();
	return "OK";
}

const char* LockCommand::VERB = "LOCK";
std::string LockCommand::execute(const std::string& verb, std::istringstream& input) {
	write(LockCommand::VERB, input);
	status().locked = true;
	return "OK";
}

const char* UnlockCommand::VERB = "UNLOCK";
std::string UnlockCommand::execute(const std::string& verb, std::istringstream& input) {
	remove(LockCommand::VERB);
	status().locked = false;
	return "OK";
}
