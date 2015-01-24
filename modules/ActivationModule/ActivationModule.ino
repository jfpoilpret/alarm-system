#include <Cosa/Watchdog.hh>

#include "WDTAlarm.hh"

#include "ActivationKeypad.hh"
#include "ActivationNetwork.hh"
#include "LedPanel.hh"

#include "PingTask.hh"
#include "VoltageNotificationTask.hh"
#include "LockNotificationTask.hh"

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
// - LED low powering	  64ms
// - WDTAlarm			1024ms
static const uint16_t WATCHDOG_PERIOD = 64;

//The setup function is called once at startup of the sketch
void setup()
{
	// Initialize power settings
	Power::twi_disable();
	Power::timer1_disable();
	Power::timer2_disable();
	Power::usart0_disable();
	// ADC is used to get the voltage level
//	Power::adc_disable();
	// Timer0 is used by intermittent RTC, no need to disable/re-enable it all the time
//	Power::timer0_disable();
	// SPI is used by NRF24L01
//	Power::spi_disable();

	// Sleep modes by order of increasing consumption
	// Lowest consumption mode (works on Arduino, not tested yet on breadboard ATmega)
	Power::set(SLEEP_MODE_PWR_DOWN);		// 0.36mA

//	Power::set(SLEEP_MODE_STANDBY);			// 0.84mA
//	Power::set(SLEEP_MODE_PWR_SAVE);		// 1.65mA
//	Power::set(SLEEP_MODE_EXT_STANDBY);		// 1.65mA
//	Power::set(SLEEP_MODE_ADC);				// 6.5 mA

	// Only this mode works when using serial output and RTC
//	Power::set(SLEEP_MODE_IDLE);			// 15mA

	// Additional setup for transmitter goes here...

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
