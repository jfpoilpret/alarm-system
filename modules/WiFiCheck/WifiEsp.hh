#ifndef WIFIESP_HH
#define	WIFIESP_HH

#include <Cosa/IOStream.hh>
#include "initializer_list"

//TODO add begin to better manage actual work of module
//TODO include powering pin + API
//TODO include reset pin + API
//TODO better wait for init
//TODO restart when issues occur (callback system)
class WiFiEsp
{
public:
	WiFiEsp(IOStream& esp, uint32_t timeout, bool debug = false);

	virtual bool begin();
	
	bool reset()
	{
		return _at({"AT+RST"}, "ready");
	}
	
	bool connect(const char* access_point, const char* password)
	{
		return _init && _at({"AT+CWJAP_CUR=\"", access_point, "\",\"", password, "\""}) && _at({"AT+CIPMODE=1"});
	}
	
	template<typename FEED> bool send(const char* host, uint16_t port, FEED& feed);

protected:
	virtual void on_timeout() {}
	
private:
	bool _at(	std::initializer_list<const char*> commands, 
				const char* expected_success = "OK",
				const char* expected_error = "ERROR");
	
	IOStream& _esp;
	const uint32_t _timeout;
	const bool _debug;
	bool _init;
	bool _handling_timeout;
};

template<typename FEED>
bool WiFiEsp::send(const char* host, uint16_t port, FEED& feed)
{
	char port2[5+1];
	if (_init &&
		_at({"AT+CIPSTART=\"TCP\",\"", host, "\",", utoa(port, port2, 10)}) &&
		_at({"AT+CIPSEND"}))
	{
		const uint8_t* content = nullptr;
		uint16_t size = 0;
		while ((content = feed(size)) != nullptr)
		{
			for (uint16_t i = 0; i < size; ++i)
				_esp.device()->putchar(*content++);
			_esp << flush;
		}
		delay(50);
		_esp << "+++" << flush;
		delay(50);
		_at({"AT+CIPCLOSE"});
		// Necessary delay to ensure trace buffer is emptied
		if (_debug)
			delay(20);
		return true;
	}
	return false;
}

#endif	/* WIFIESP_HH */
