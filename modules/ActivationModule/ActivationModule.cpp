#include <Cosa/Watchdog.hh>

#include "ActivationKeypad.hh"
#include "ActivationNetwork.hh"
#include "LedPanel.hh"

#include "CommonTasks.hh"
#include "PingTask.hh"
#include "LockNotificationTask.hh"

//TODO Externalize these constants?
const uint16_t NETWORK = 0xC05A;
const uint8_t SERVER_ID = 0x01;
const uint8_t MODULE_ID = 0x10;

const uint32_t PING_PERIOD_SEC = 5;
const uint32_t VOLTAGE_PERIOD_SEC = 60;
//const uint32_t VOLTAGE_PERIOD_SEC = 3600;

// Watchdog period must be the minimum of periods required by all watchdog timer users:
// - keypad scan		  64ms
// - LED low powering	  16ms
// - Alarm				  1024ms
static const uint16_t WATCHDOG_PERIOD = 16;

// Get the device ID from DIP switch pins
uint8_t readConfigId()
{
	InputPin::mode(CONFIG_ID1, InputPin::Mode::PULLUP_MODE);
	InputPin::mode(CONFIG_ID2, InputPin::Mode::PULLUP_MODE);
	uint8_t id = (InputPin::read(CONFIG_ID1) ? 0: 1);
	id += (InputPin::read(CONFIG_ID2) ? 0 : 2);
	InputPin::mode(CONFIG_ID1, InputPin::Mode::NORMAL_MODE);
	InputPin::mode(CONFIG_ID2, InputPin::Mode::NORMAL_MODE);
	return id;
}

int main()
{
	// Disable analog comparator
	ACSR = _BV(ACD);
	// Disable all modules but ADC (required for bandgap reading)
	Power::all_disable();
	Power::adc_enable();
	// Allow interrupts from here
	sei();

	// Sleep modes by order of increasing consumption
	// Lowest consumption mode (works on Arduino, not tested yet on breadboard ATmega)
	Power::set(SLEEP_MODE_PWR_DOWN);		// 0.36mA
	// Only this mode works when using serial output and full-time RTC
//	Power::set(SLEEP_MODE_IDLE);			// 15mA

	// Needed for Periodics and Alarms to work properly
	Watchdog::Scheduler scheduler;
	Watchdog::Clock clock;

	// Declare sensors and actuators
	LedPanel ledPanel(&scheduler);
	ActivationTransmitter transmitter(SERVER_ID);

	// Declare listeners
	LockNotificationTask lockTask(transmitter, ledPanel);
	ActivationKeypad keypad(&scheduler, &lockTask);

	// Declare periodic tasks
	PingTask pingTask(&clock, PING_PERIOD_SEC, transmitter, ledPanel);
	VoltageNotificationTask voltageTask(&clock, VOLTAGE_PERIOD_SEC, transmitter);

	// Additional setup for transmitter goes here...
	transmitter.begin(NETWORK, MODULE_ID + readConfigId());

	// Start watchdog and keypad
	Watchdog::begin(WATCHDOG_PERIOD);

	// Start all tasks
	keypad.start();
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
