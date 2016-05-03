#include <Cosa/Alarm.hh>
#include <Cosa/IOBuffer.hh>
#include <Cosa/RTT.hh>
#include <Cosa/Trace.hh>
#include <Cosa/UART.hh>
#ifndef BOARD_ATMEGA2560
#	include <Cosa/Soft/UART.hh>
#endif
#include <Cosa/Watchdog.hh>
//#include <stdint-gcc.h>
#include "Camera.hh"

static const uint16_t WATCHDOG_PERIOD = 16;

static const uint32_t SEND_PERIOD_SECS = 60;
static const uint32_t CAM_REPLY_TIMEOUT_SECS = 2;

static const size_t CAM_RX_BUFFER_MAX = 64;
static const size_t CAM_TX_BUFFER_MAX = 16;

static const size_t CAM_PICT_BUFFER_SIZE = 64;
//static const size_t CAM_PICT_BUFFER_SIZE = 32;

static const Board::DigitalPin CAM_TX_PIN = Board::D2;
static const Board::InterruptPin CAM_RX_PIN = Board::PCI3;

class CamHandler: public Alarm
{
public:
	CamHandler(Camera& cam, ::Clock* clock, uint32_t period)
		:Alarm(clock, period), _cam(cam), _led(Board::LED, 0)
	{
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
//		trace << "picture size = " << size << endl;
		uint16_t address = 0;
		while (size > 0)
		{
			uint8_t buffer[CAM_PICT_BUFFER_SIZE];
			_cam.picture_content(address, CAM_PICT_BUFFER_SIZE, buffer);
			address += CAM_PICT_BUFFER_SIZE;
			size -= CAM_PICT_BUFFER_SIZE;
			trace.device()->write(buffer, CAM_PICT_BUFFER_SIZE);
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
	
#ifdef BOARD_ATMEGA2560
	IOBuffer<CAM_RX_BUFFER_MAX> ibuf;
	IOBuffer<CAM_TX_BUFFER_MAX> obuf;
	UART uartCam{1, &ibuf, &obuf};
#else
	IOBuffer<CAM_RX_BUFFER_MAX> ibuf;
	Soft::UART uartCam{CAM_TX_PIN, CAM_RX_PIN, &ibuf};
#endif
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
