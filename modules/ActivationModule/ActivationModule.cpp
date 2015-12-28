#include <Cosa/Watchdog.hh>

#include "ActivationKeypad.hh"
#include "ActivationNetwork.hh"
#include "LedPanel.hh"

#include "PingTask.hh"
#include "VoltageNotificationTask.hh"
#include "LockNotificationTask.hh"

#include "RTCAdapter.hh"

//TODO Externalize these constants?
const uint16_t NETWORK = 0xC05A;
const uint8_t SERVER_ID = 0x01;
const uint8_t MODULE_ID = 0x10;

const uint32_t PING_PERIOD_SEC = 5;
const uint32_t VOLTAGE_PERIOD_SEC = 60;
//const uint32_t VOLTAGE_PERIOD_SEC = 3600;

// Needed for Periodics and Alarms to work properly
static Watchdog::Scheduler scheduler;
static Watchdog::Clock clock;

// Declare sensors and actuators
static LedPanel ledPanel(&scheduler);
static ActivationTransmitter transmitter(NETWORK, MODULE_ID, SERVER_ID);
static ActivationKeypad keypad(&scheduler);

// Declare listeners
static LockNotificationTask lockTask(transmitter, ledPanel);

// Declare periodic tasks
static PingTask pingTask(&clock, PING_PERIOD_SEC, transmitter, ledPanel);
static VoltageNotificationTask voltageTask(&clock, VOLTAGE_PERIOD_SEC, transmitter);

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

//The setup function is called once at startup of the sketch
void setup()
{
	// Initialize power settings: disable every unneeded component
	Power::twi_disable();
	Power::timer0_disable();
	Power::timer1_disable();
	Power::usart0_disable();
	// ADC is used to get the voltage level
	// Timer2 is used by intermittent new RTT, no need to disable/re-enable it all the time
	// SPI is used by NRF24L01
//	Power::adc_disable();
//	Power::timer2_disable();
//	Power::spi_disable();

	// Sleep modes by order of increasing consumption
	// Lowest consumption mode (works on Arduino, not tested yet on breadboard ATmega)
	Power::set(SLEEP_MODE_PWR_DOWN);		// 0.36mA
//	Power::set(SLEEP_MODE_STANDBY);			// 0.84mA
//	Power::set(SLEEP_MODE_PWR_SAVE);		// 1.65mA
//	Power::set(SLEEP_MODE_EXT_STANDBY);		// 1.65mA
//	Power::set(SLEEP_MODE_ADC);				// 6.5 mA
	// Only this mode works when using serial output and full-time RTC
//	Power::set(SLEEP_MODE_IDLE);			// 15mA

	// Additional setup for transmitter goes here...
	transmitter.address(NETWORK, MODULE_ID + readConfigId());

	keypad.attachListener(&lockTask);

	// Start watchdog and keypad
	Watchdog::begin(WATCHDOG_PERIOD);

	// Start all tasks
	keypad.start();
	pingTask.start();
	voltageTask.start();
}

// The loop function is called in an endless loop
void loop()
{
	Watchdog::await();

	Event event;
	while (Event::queue.dequeue(&event))
		event.dispatch();
}
