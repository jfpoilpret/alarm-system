#ifndef WIFIESP_HH
#define	WIFIESP_HH

#include <Cosa/IOStream.hh>
#include "initializer_list"

class WiFiEsp
{
public:
	WiFiEsp(IOStream& esp, uint32_t timeout);

	bool reset()
	{
		return _at({"AT+RST"}, "ready");
	}
	
	bool connect(const char* access_point, const char* password)
	{
		return _at({"AT+CWJAP_CUR=\"", access_point, "\",\"", password, "\""}) && _at({"AT+CIPMODE=1"});
	}
	
	template<typename FEED> bool send(const char* host, uint16_t port, FEED& feed);
	
private:
	bool _at(	std::initializer_list<const char*> commands, 
				const char* expected_success = "OK",
				const char* expected_error = "ERROR");
	
	const uint32_t _timeout;
	IOStream& _esp;
	bool _init;
};

template<typename FEED>
bool WiFiEsp::send(const char* host, uint16_t port, FEED& feed)
{
	char port2[5+1];
	if (_at({"AT+CIPSTART=\"TCP\",\"", host, "\",", utoa(port, port2, 10)}) &&
		_at({"AT+CIPSEND"}))
	{
		//TODO improve feeding and ensure all is transmitted as bytes
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
		delay(20);
		return true;
	}
	return false;
}
	

#endif	/* WIFIESP_HH */

