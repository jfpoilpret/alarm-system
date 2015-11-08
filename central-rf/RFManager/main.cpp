/* 
 * File:   main.cpp
 *
 * Main entry point of Alarm System central process to communicate to sensor devices through NRF24L01 chip.
 * This process is used to communicate with all devices and proxy all exchanges from/to the web system 
 * on Raspbery Pi (Python-based).
 */

#include <sys/stat.h>
#include "RFManager.h"

static void create_temp_dir() {
	struct stat sb;
	if (stat("/tmp/alarm-system", &sb)) {
		// Directory does not exist, create it first
		mkdir("/tmp/alarm-system", 0777);
	}
}

int main(int argc, char** argv) {
	// Ensure temp dir exists (used for ZMQ IPC file descriptors)
	create_temp_dir();
	
	AlarmStatus status;
	zmq::context_t context(1);
	CommandManager manager(context, status);
	
	// Block until exit
	manager.block_until_exit();
	return 0;
}
