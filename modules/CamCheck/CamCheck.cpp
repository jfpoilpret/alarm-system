#include <Cosa/Alarm.hh>
#include <Cosa/IOBuffer.hh>
#include <Cosa/RTT.hh>
#include <Cosa/Trace.hh>
#include <Cosa/UART.hh>
#include <Cosa/Soft/UART.hh>
#include <Cosa/Watchdog.hh>
#include <stdint-gcc.h>
#include "initializer_list"

static const uint16_t WATCHDOG_PERIOD = 16;

static const uint32_t SEND_PERIOD_SECS = 60;
static const uint32_t CAM_REPLY_TIMEOUT_SECS = 2;

static const size_t CAM_RX_BUFFER_MAX = 64;
static const size_t CAM_TX_BUFFER_MAX = 16;

static const size_t CAM_RECV_BUFFER_SIZE = 16;
static const size_t CAM_PICT_BUFFER_SIZE = 32;

static const Board::DigitalPin CAM_TX_PIN = Board::D2;
static const Board::InterruptPin CAM_RX_PIN = Board::PCI3;

static uint8_t HI(uint16_t in)
{
	return (in >> 8);
}

static uint8_t LO(uint16_t in)
{
	return (in & 0xFF);
}

static uint16_t SWAP(uint16_t in)
{
	return (LO(in) << 8) | HI(in);
}

class Camera
{
public:
	enum class Resolution
	{
		RES_640x480,
		RES_320x240,
		RES_160x120,
	};
	
	enum class BaudRate
	{
		BAUD_9600,
		BAUD_19200,
		BAUD_38400,
		BAUD_57600,
		BAUD_115200
	};
	
	Camera(IOStream& cam, uint32_t timeout)
		:_timeout(timeout * 1000), _cam(cam)
	{
		delay(3000);
		_trace(true);
	}
	
	void reset()
	{
//		trace << "reset" << endl;
		_send({0x56, 0x00, 0x26, 0x00});
		_receive({0x76, 0x00, 0x26, 0x00, 0x00});
		//FIXME reset generates the power on init string: we should wait until it is received then!
		delay(3000);
//		_trace(true);
	}
	
	//TODO method to take picture and notify callback for content
	template<typename CB>
	void take_picture(CB& callback)
	{
		take_picture();
		int32_t size = picture_size();
		uint16_t address = 0;
		while (size > 0)
		{
			//TODO buffer should be an argument to the function (more customizable)
			uint8_t buffer[CAM_PICT_BUFFER_SIZE];
			picture_content(address, CAM_PICT_BUFFER_SIZE, buffer);
			address += CAM_PICT_BUFFER_SIZE;
			size -= CAM_PICT_BUFFER_SIZE;
			callback(buffer, CAM_PICT_BUFFER_SIZE, (size > 0));
		}
		stop_picture();
	}
	
	void take_picture()
	{
//		trace << "take_picture" << endl;
		_send({0x56, 0x00, 0x36, 0x01, 0x00});
		_receive({0x76, 0x00, 0x36, 0x00, 0x00});
	}
	
	void stop_picture()
	{
//		trace << "stop_picture" << endl;
		_send({0x56, 0x00, 0x36, 0x01, 0x03});
		_receive({0x76, 0x00, 0x36, 0x00, 0x00});
	}
	
	uint16_t picture_size()
	{
//		trace << "get picture_size" << endl;
		_send({0x56, 0x00, 0x34, 0x01, 0x00});
		uint16_t size;
		if (	_receive({0x76, 0x00, 0x34, 0x00, 0x04, 0x00, 0x00})
			&&	_receive((uint8_t*)(&size), sizeof(size)))
			return SWAP(size);
		return 0;
	}
	
	void picture_content(uint16_t address, uint16_t size, uint8_t* buffer)
	{
		_send({
			0x56, 0x00, 0x32, 0x0C, 0x00, 0x0A, 
			0x00, 0x00, HI(address), LO(address), 
			0x00, 0x00, HI(size), LO(size), 
			0x00, 0x0A});
		_receive({0x76, 0x00, 0x32, 0x00, 0x00}) &&
		_receive(buffer, size) &&
		_receive({0x76, 0x00, 0x32, 0x00, 0x00});
	}
	
	void compression(uint8_t ratio)
	{
		_send({0x56, 0x00, 0x31, 0x05, 0x01, 0x01, 0x12, 0x04, ratio});
		_receive({0x76, 0x00, 0x31, 0x00, 0x00});
	}
	
	void picture_resolution(Resolution resolution)
	{
		uint8_t code;
		switch (resolution)
		{
			case Resolution::RES_160x120: code = 0x22; break;
			case Resolution::RES_320x240: code = 0x11; break;
			case Resolution::RES_640x480: code = 0x00; break;
		}
		_send({0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19, code});
		_receive({0x76, 0x00, 0x31, 0x00, 0x00});
	}
	
	void enter_power_save()
	{
//		trace << "enter_power_save" << endl;
		_send({0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x01});
		_receive({0x76, 0x00, 0x3E, 0x00, 0x00});
	}
	
	void exit_power_save()
	{
//		trace << "exit_power_save" << endl;
		_send({0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x00});
		_receive({0x76, 0x00, 0x3E, 0x00, 0x00});
	}
	
	void baud_rate(BaudRate baud)
	{
		uint16_t code;
		switch (baud)
		{
			case BaudRate::BAUD_9600: code = 0xAEC8; break;
			case BaudRate::BAUD_19200: code = 0x56E4; break;
			case BaudRate::BAUD_38400: code = 0x2AF2; break;
			case BaudRate::BAUD_57600: code = 0x1C4C; break;
			case BaudRate::BAUD_115200: code = 0x0DA6; break;
		}
		_send({
			0x56, 0x00, 0x24, 0x03, 0x01, 
			HI(code), LO(code)});
		_receive({0x76, 0x00, 0x24, 0x00, 0x00});
	}
	
private:
	void _send(std::initializer_list<uint8_t> content)
	{
		for (auto i : content)
			_cam.device()->putchar(i);
		_cam.device()->flush();
	}
	
	bool _receive(std::initializer_list<uint8_t> expected)
	{
		uint8_t content[CAM_RECV_BUFFER_SIZE];
		if (_receive(content, expected.size()))
		{
			uint8_t* compare = content;
			for (auto i : expected)
			{
				if (*compare != i)
				{
					trace << "expected " << hex << i << ", actual " << *compare << endl;
					return false;
				}
				++compare;
			}
			return true;
		}
		return false;
	}

	bool _receive(uint8_t* content, uint8_t size)
	{
		// Wait until timeout or expected received
		uint32_t now = RTT::millis();
		uint8_t count = 0;
		do
		{
			while (_cam.device()->available())
			{
				*content++ = _cam.device()->getchar();
				if (++count == size)
					return true;
			}
			delay(1);
		}
		while (RTT::since(now) < _timeout);
		trace << "receive timeout. Expected size " << size << ", actual " << count << endl;
		return false;
	}

	void _trace(bool ascii_response = false)
	{
		trace << "<< ";
		while (_cam.device()->available()) 
		{
			int c = _cam.device()->getchar();
			if (ascii_response)
				trace << (char) c;
			else
				trace << hex << c << ' ';
		}
		trace << endl;
	}

	const uint32_t _timeout;
	IOStream& _cam;
};


class CamHandler: public Alarm
{
public:
	CamHandler(Camera& cam, ::Clock* clock, uint32_t period)
		:Alarm(clock, period), _cam(cam), _led(Board::LED, 0)
	{
		cam.reset();
		cam.compression(0x36);
		cam.picture_resolution(Camera::Resolution::RES_640x480);
		cam.reset();
	}
	
	virtual void run()
	{
		_led.toggle();
		_cam.exit_power_save();
		_cam.take_picture();
		int32_t size = _cam.picture_size();
		trace << "picture size = " << size << endl;
		uint16_t address = 0;
		while (size > 0)
		{
			uint8_t buffer[CAM_PICT_BUFFER_SIZE];
			_cam.picture_content(address, CAM_PICT_BUFFER_SIZE, buffer);
			address += CAM_PICT_BUFFER_SIZE;
			size -= CAM_PICT_BUFFER_SIZE;
		}
		_cam.stop_picture();
		_cam.enter_power_save();
		// This delay seems necessary to avoid garbage sent to trace... (1ms is not long enough)
		delay(5);
	}
	
private:
	Camera& _cam;
	OutputPin _led;
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
	
	uart.begin(115200);
	trace.begin(&uart, PSTR("CamCheck: started"));
	
	IOBuffer<CAM_RX_BUFFER_MAX> ibuf;

	Soft::UART uartCam{CAM_TX_PIN, CAM_RX_PIN, &ibuf};
	uartCam.begin(38400);
	IOStream streamCam{&uartCam};
	Camera camera{streamCam, CAM_REPLY_TIMEOUT_SECS};
	
	//TODO improve baud rate here
//	camera.baud_rate(Camera::BaudRate::BAUD_115200);
//	uartCam.end();
//	uartCam.begin(115200);
	
	// Needed for Alarms to work properly
	Watchdog::Clock clock;
	CamHandler handler(camera, &clock, SEND_PERIOD_SECS);
	
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
