#include <Cosa/Alarm.hh>
#include <Cosa/IOBuffer.hh>
#include <Cosa/RTT.hh>
#include <Cosa/Trace.hh>
#include <Cosa/UART.hh>
#include <Cosa/Watchdog.hh>
#include <stdint-gcc.h>

#include "Camera.hh"
#include "WifiEsp.hh"

#if 0
// In the following header, define credentials as follows:
static const char* WIFI_AP = "ACCESS-POINT";
static const char* WIFI_PASSWORD = "PASSWORD";
#endif
// The following header is not committed as it contains WIFI credentials
#include "Credentials.hh"

// Board features usage
static const Board::DigitalPin ESP_RESET = Board::D7;
static const uint8_t ESP_UART = 2;
static const uint8_t CAM_UART = 1;

static const uint16_t WATCHDOG_PERIOD = 16;
//static const uint16_t WATCHDOG_PERIOD = 1024;

static const uint32_t SEND_PERIOD_SECS = 60;

static const uint32_t ESP_AT_REPLY_TIMEOUT_SECS = 10;
static const size_t ESP_RX_BUFFER_MAX = 256;
static const size_t ESP_TX_BUFFER_MAX = 64;

static const uint32_t CAM_REPLY_TIMEOUT_SECS = 2;
static const size_t CAM_RX_BUFFER_MAX = 64;
static const size_t CAM_TX_BUFFER_MAX = 16;

class AutoResetWiFiEsp: public WiFiEsp
{
public:
	AutoResetWiFiEsp(const Board::DigitalPin esp_reset, IOStream& esp, uint32_t timeout, bool debug = false)
		:WiFiEsp{esp, timeout, debug}, _esp_reset{esp_reset, 1} {}

	virtual bool begin()
	{
		trace << "begin() #1" << endl;
		hard_reset();
		trace << "begin() #2" << endl;
		bool result = WiFiEsp::begin();
		trace << "begin() #3 " << result << endl;
		if (result)
		{
			result = connect(WIFI_AP, WIFI_PASSWORD);
			trace << "begin() #4 " << result << endl;
		}
		return result;
//		return WiFiEsp::begin() && connect(WIFI_AP, WIFI_PASSWORD);
	}
	
	void hard_reset()
	{
		_esp_reset._clear();
		delay(100);
		_esp_reset._set();
		delay(100);
	}
	
protected:
	virtual void on_timeout()
	{
		begin();
	}

private:
	OutputPin _esp_reset;
};

class WiFiHandler: public Alarm
{
public:
	WiFiHandler(WiFiEsp& wifi, Camera& camera, ::Clock* clock, uint32_t period)
		:Alarm{clock, period}, _wifi(wifi), _camera(camera), _led{Board::LED, 0}
	{
//		_wifi.connect(WIFI_AP, WIFI_PASSWORD);
		_camera.enter_power_save();
	}
	
	virtual void run()
	{
		_led.toggle();

		// Prepare camera for taking picture
		_camera.exit_power_save();
		_camera.take_picture();

		// Feed picture payload to WIFI
		PictureFeeder feeder{_camera};
		_wifi.send("192.168.0.111", 9999U, feeder);

		_camera.stop_picture();
		_camera.enter_power_save();
		// This delay seems necessary to avoid garbage sent to trace... (1ms is not long enough)
		delay(5);
	}
	
private:
	class PictureFeeder
	{
	public:
		PictureFeeder(Camera& camera):_camera(camera), _size{_camera.picture_size()}, _address{}
		{
			trace << "picture size = " << _size << endl;
		}
		
		const uint8_t* operator()(uint16_t& size)
		{
			if (_size > 0)
			{
				_camera.picture_content(_address, PAYLOAD_SIZE, _payload);
				_address += PAYLOAD_SIZE;
				_size -= PAYLOAD_SIZE;
				size = PAYLOAD_SIZE;
//				trace.device()->write(_payload, PAYLOAD_SIZE);
				return _payload;
			}
			size = 0;
			return nullptr;
		}
		
	private:
		static const uint16_t PAYLOAD_SIZE = 64;
		Camera& _camera;
		int32_t _size;
		uint16_t _address;
		uint8_t _payload[PAYLOAD_SIZE];
	};
	
	WiFiEsp& _wifi;
	Camera& _camera;
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
	// This delay is only to give me time to open serial monitor for traces after board reset...
	delay(10000);
	
	uart.begin(115200);
	trace.begin(&uart, PSTR("WiFiCheck: started"));
	
	IOBuffer<ESP_RX_BUFFER_MAX> esp_ibuf;
	IOBuffer<ESP_TX_BUFFER_MAX> esp_obuf;
	UART esp_uart{ESP_UART, &esp_ibuf, &esp_obuf};
	esp_uart.eol(IOStream::Mode::CRLF_MODE);
	esp_uart.begin(115200);
	IOStream esp_stream(&esp_uart);
	AutoResetWiFiEsp wifi{ESP_RESET, esp_stream, ESP_AT_REPLY_TIMEOUT_SECS, true};
	// Reset and start ESP8266
	wifi.begin();

	IOBuffer<CAM_RX_BUFFER_MAX> cam_ibuf;
	IOBuffer<CAM_TX_BUFFER_MAX> cam_obuf;
	UART cam_uart{CAM_UART, &cam_ibuf, &cam_obuf};
	cam_uart.begin(38400);
	IOStream cam_stream{&cam_uart};
	Camera camera{cam_stream, CAM_REPLY_TIMEOUT_SECS};
	// Change initial settings that need a reset
	// Transmission time divided by 4 with this resolution, pictures still OK
	camera.picture_resolution(Camera::Resolution::RES_320x240);
	// Must reset camera after changing resolution
	camera.reset();
	// Change initial settings that are changed back to default after reset
	// Change baud rate to improve speed
	trace << "Change baud rate" << endl;
	camera.baud_rate(Camera::BaudRate::BAUD_230400);
	cam_uart.end();
	cam_uart.begin(230400);
	// NOTE: I'm not sure this delay is necessary, but it works...
	delay(100);
	// Set higher compression rate with good enough image quality 
	camera.compression(0x80);
	
	// Needed for Alarms to work properly
	Watchdog::Clock clock;
	WiFiHandler handler(wifi, camera, &clock, SEND_PERIOD_SECS);
	
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
