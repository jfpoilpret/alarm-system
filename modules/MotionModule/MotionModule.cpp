#include <Cosa/InputPin.hh>
#include <Cosa/Watchdog.hh>

#include "Pins.hh"
#include "MotionNetwork.hh"

#include "CommonTasks.hh"
#include "MotionDetector.hh"

//TODO Externalize these constants?
const uint16_t NETWORK = 0xC05A;
const uint8_t SERVER_ID = 0x01;
const uint8_t MODULE_ID = 0x20;

const uint32_t PING_PERIOD_SEC = 5;
const uint32_t VOLTAGE_PERIOD_SEC = 60;
//const uint32_t VOLTAGE_PERIOD_SEC = 3600;

// Watchdog period must be the minimum of periods required by all watchdog timer users:
// - Alarm				  1024ms
static const uint16_t WATCHDOG_PERIOD = 1024;

// Get the device ID from DIP switch pins
uint8_t readConfigId()
{
//	InputPin::mode(CONFIG_ID1, InputPin::Mode::PULLUP_MODE);
//	InputPin::mode(CONFIG_ID2, InputPin::Mode::PULLUP_MODE);
//	uint8_t id = (InputPin::read(CONFIG_ID1) ? 0: 1);
//	id += (InputPin::read(CONFIG_ID2) ? 0 : 2);
//	InputPin::mode(CONFIG_ID1, InputPin::Mode::NORMAL_MODE);
//	InputPin::mode(CONFIG_ID2, InputPin::Mode::NORMAL_MODE);
//	return id;
	return 0;
}

int main()
{
	// Disable analog comparator
	ACSR = _BV(ACD);
	// Disable all modules
	Power::all_disable();
	// Allow interrupts from here
	sei();

	// First wait 1 minute for PIR sensor to stabilize
//	sleep(60);//TODO add constant!!!
	
	// Sleep modes by order of increasing consumption
	// Lowest consumption mode (works on Arduino, not tested yet on breadboard ATmega)
	Power::set(SLEEP_MODE_PWR_DOWN);		// 0.36mA
	// Only this mode works when using serial output and full-time RTC
//	Power::set(SLEEP_MODE_IDLE);			// 15mA

	// Needed for Alarms to work properly
	Watchdog::Clock clock;

	// Declare sensors and actuators
	MotionTransmitter transmitter(SERVER_ID);
	MotionDetector detector(&transmitter);

	// Declare periodic tasks
	DefaultPingTask pingTask(&clock, PING_PERIOD_SEC, transmitter);
	VoltageNotificationTask voltageTask(&clock, VOLTAGE_PERIOD_SEC, transmitter);

	// Additional setup for transmitter goes here...
	transmitter.address(NETWORK, MODULE_ID + readConfigId());

	// Start watchdog
	Watchdog::begin(WATCHDOG_PERIOD);

	// Start all tasks
	PinChangeInterrupt::begin();
	detector.enable();
	pingTask.start();
	voltageTask.start();

	while (true)
	{
		Watchdog::await();

		Event event;
		while (Event::queue.dequeue(&event))
			event.dispatch();
	}
}
