#include <Cosa/RTT.hh>
#include <Cosa/Trace.hh>
#include <stdint-gcc.h>
#include "WifiEsp.hh"

static const size_t MAX_LINE_LEN = 80;

WiFiEsp::WiFiEsp(IOStream& esp, uint32_t timeout, bool debug)
	:_esp(esp), _timeout(timeout * 1000), _debug(debug), _init(false), _handling_timeout(false) {}

bool WiFiEsp::begin()
{
	_init = reset() && _at({"AT+CWMODE_CUR=1"});
	return _init;
}

bool WiFiEsp::_at(	std::initializer_list<const char*> commands, 
					const char* expected_success,
					const char* expected_error)
{
	// Check if something in RX buffer
	_esp.device()->empty();
	for (auto cmd: commands)
		_esp << cmd;
	_esp << endl << flush;
	if (_debug)
	{
		for (auto cmd: commands)
			trace << cmd;
		trace << " sent" << endl;
	}
	// Wait for expected reply until timeout
	uint32_t now = RTT::millis();
	do
	{
		char buffer[MAX_LINE_LEN + 1];
		buffer[0] = 0;
		char* line = _esp.readline(buffer, MAX_LINE_LEN, false);
		if (line && strlen(line))
		{
			// Remove \n before echo
			line[strlen(line) - 1] = 0;
			if (_debug)
				trace << line << endl;

			if (strstr(line, expected_success)) return true;
			if (strstr(line, expected_error)) return false;
		}
		delay(1);
	}
	while (RTT::since(now) < _timeout);
	if (_debug)
		trace << "_at() timeout" << endl;
	//FIXME do something here to restore connection...
	if (!_handling_timeout)
	{
		_handling_timeout = true;
		on_timeout();
		_handling_timeout = false;
	}
	return false;
}
