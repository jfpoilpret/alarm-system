#include <Cosa/Watchdog.hh>

#include "WDTAlarm.hh"

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

// Needed for Alarms to work properly
static WDTAlarm::Scheduler scheduler;

// Declare sensors and actuators
static LedPanel ledPanel;
static ActivationTransmitter transmitter(NETWORK, MODULE_ID, SERVER_ID);
static ActivationKeypad keypad;

// Declare listeners
static LockNotificationTask lockTask(transmitter, ledPanel);

// Declare periodic tasks
static PingTask pingTask(PING_PERIOD_SEC, transmitter, ledPanel);
static VoltageNotificationTask voltageTask(VOLTAGE_PERIOD_SEC, transmitter);

// Watchdog period must be the minimum of periods required by all watchdog timer users:
// - keypad scan		  64ms
// - LED low powering	  32ms
// - WDTAlarm			1024ms
static const uint16_t WATCHDOG_PERIOD = 32;

// Get the device ID from DIP switch pins
uint8_t readConfigId()
{
	InputPin::set_mode(CONFIG_ID1, InputPin::Mode::PULLUP_MODE);
	InputPin::set_mode(CONFIG_ID2, InputPin::Mode::PULLUP_MODE);
	uint8_t id = (InputPin::read(CONFIG_ID1) ? 0: 1);
	id += (InputPin::read(CONFIG_ID2) ? 0 : 2);
	InputPin::set_mode(CONFIG_ID1, InputPin::Mode::NORMAL_MODE);
	InputPin::set_mode(CONFIG_ID2, InputPin::Mode::NORMAL_MODE);
	return id;
}

//The setup function is called once at startup of the sketch
void setup()
{
	// Initialize power settings: disable every unneeded component
	Power::twi_disable();
	Power::timer1_disable();
	Power::timer2_disable();
	Power::usart0_disable();
	// ADC is used to get the voltage level
	// Timer0 is used by intermittent RTC, no need to disable/re-enable it all the time
	// SPI is used by NRF24L01
//	Power::adc_disable();
//	Power::timer0_disable();
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

	// Initialize RTC adapter properly
	RTCAdapter::init();

	// Additional setup for transmitter goes here...
	transmitter.set_address(NETWORK, MODULE_ID + readConfigId());

	// Start all tasks
	pingTask.enable();
	voltageTask.enable();

	keypad.attachListener(&lockTask);

	// Start watchdog and keypad
	Watchdog::begin(WATCHDOG_PERIOD, Watchdog::push_timeout_events);
	scheduler.begin();
	keypad.begin();
	pingTask.enable();
}

// The loop function is called in an endless loop
void loop()
{
	Watchdog::await();

	Event event;
	while (Event::queue.dequeue(&event))
		event.dispatch();
}
