#include <Cosa/Alarm.hh>
#include <Cosa/IOBuffer.hh>
#include <Cosa/RTT.hh>
#include <Cosa/Trace.hh>
#include <Cosa/UART.hh>
#include <Cosa/Watchdog.hh>
#include <stdint-gcc.h>

#include "WifiEsp.hh"

#if 0
// In the following header, define credentials as follows:
static const char* WIFI_AP = "ACCESS-POINT";
static const char* WIFI_PASSWORD = "PASSWORD";
#endif
// The following header is not committed as it contains WIFI credentials
#include "Credentials.hh"

static const uint16_t WATCHDOG_PERIOD = 16;
//static const uint16_t WATCHDOG_PERIOD = 1024;

static const uint32_t SEND_PERIOD_SECS = 60;
static const uint32_t AT_REPLY_TIMEOUT_SECS = 10;
static const size_t MAX_LINE_LEN = 80;

static const size_t ESP_RX_BUFFER_MAX = 256;
static const size_t ESP_TX_BUFFER_MAX = 64;

static const char* PAYLOAD = "    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345\n";

class WiFiHandler: public Alarm
{
public:
	WiFiHandler(WiFiEsp& esp, ::Clock* clock, uint32_t period)
		:Alarm(clock, period), _esp(esp), _led(Board::LED, 0)
	{
		_esp.connect(WIFI_AP, WIFI_PASSWORD);
	}
	
	virtual void run()
	{
		_led.toggle();
		// Pass functor that sends 20 times the same string
		Feeder feeder{20};
		_esp.send("192.168.0.107", 9999U, feeder);
	}
	
private:
	class Feeder
	{
	public:
		Feeder(uint8_t units_count):_units_count(units_count), _unit_size(strlen(PAYLOAD)), _index(0)
		{
			memcpy(_payload, PAYLOAD, _unit_size);
		}
		
		const uint8_t* operator()(uint16_t& size)
		{
			if (_index < _units_count)
			{
				itoa(_index, (char*) _payload, 10);
				++_index;
				size = _unit_size;
				return _payload;
			}
			size = 0;
			return nullptr;
		}
		
	private:
		static const uint16_t PAYLOAD_SIZE = 64;
		const uint8_t _units_count;
		const uint16_t _unit_size;
		uint8_t _payload[PAYLOAD_SIZE];
		uint8_t _index;
	};
	
	WiFiEsp& _esp;
	OutputPin _led;
	bool _init;
};

int main()
{
	// Disable analog comparator
	ACSR = _BV(ACD);
	// Disable all modules but ADC (required for bandgap reading)
	Power::all_disable();
	Power::adc_enable();
	// Allow interrupts from here
	sei();
	
	// Start watchdog and alarms
	Watchdog::begin(WATCHDOG_PERIOD);
//	Power::set(SLEEP_MODE_PWR_DOWN);		// 5uA
	
	// Start using RTT
	RTT::begin();
	
	// Reset ESP8266
	OutputPin esp_reset = OutputPin(Board::D7, 0);
	delay(1);
	esp_reset._set();
	delay(10);
	
	uart.begin(115200);
	trace.begin(&uart, PSTR("WiFiCheck: started"));
	
	IOBuffer<ESP_RX_BUFFER_MAX> ibuf;
	IOBuffer<ESP_TX_BUFFER_MAX> obuf;

	UART uartESP(2, &ibuf, &obuf);
	uartESP.eol(IOStream::Mode::CRLF_MODE);
//	uartESP.eol(IOStream::Mode::LF_MODE);
//	uartESP.eol(IOStream::Mode::CR_MODE);
	uartESP.begin(115200);
	IOStream esp(&uartESP);
	
	WiFiEsp wifiEsp(esp, AT_REPLY_TIMEOUT_SECS);
	
	// Needed for Alarms to work properly
	Watchdog::Clock clock;
	WiFiHandler handler(wifiEsp, &clock, SEND_PERIOD_SECS);
	
	// Stop using RTT and restore Watchdog
	RTT::end();
	::delay = Watchdog::delay;

	handler.start();
	
	while (true)
	{
		Watchdog::await();

		// If there is at least one event to be dispatched, then change sleep mode, start RTT and NRF
		if (Event::queue.available())
		{
			// Only this mode works when using serial output and full-time RTC
			Power::set(SLEEP_MODE_IDLE);			// 15mA
			// Start using RTT
			RTT::begin();
			
			Event event;
			while (Event::queue.dequeue(&event))
				event.dispatch();
			
			// Stop using RTT and restore Watchdog
			RTT::end();
			::delay = Watchdog::delay;
			// Lowest consumption mode
			Power::set(SLEEP_MODE_PWR_DOWN);		// 5uA
		}
	}
}
