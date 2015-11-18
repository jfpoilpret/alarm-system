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

static InitCommand cmd_init;
static CodeCommand cmd_code;
static StartCommand cmd_start;
static LockCommand cmd_lock;
static UnlockCommand cmd_unlock;
static StopCommand cmd_stop;
static ExitCommand cmd_exit;

int main(int argc, char** argv) {
	// Ensure temp dir exists (used for ZMQ IPC file descriptors)
	create_temp_dir();
	// Initialize Manager
	AlarmStatus status;
	zmq::context_t context(1);
	CommandManager manager(context, status);
	// Setup all handlers for commands received from Web system
	manager.add_command(cmd_init.VERB, &cmd_init);
	manager.add_command(cmd_code.VERB, &cmd_code);
	manager.add_command(cmd_start.VERB, &cmd_start);
	manager.add_command(cmd_lock.VERB, &cmd_lock);
	manager.add_command(cmd_unlock.VERB, &cmd_unlock);
	manager.add_command(cmd_stop.VERB, &cmd_stop);
	manager.add_command(cmd_exit.VERB, &cmd_exit);
	// Finally start manager
	manager.start();
	// Block until exit
	manager.block_until_exit();
	return 0;
}
