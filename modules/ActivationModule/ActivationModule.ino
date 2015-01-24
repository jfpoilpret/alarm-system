#include <Cosa/Alarm.hh>
#include <Cosa/RTC.hh>
#include <Cosa/Watchdog.hh>

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
static Alarm::Scheduler scheduler;

// Declare sensors and actuators
static LedPanel ledPanel;
static ActivationTransmitter transmitter(NETWORK, MODULE_ID, SERVER_ID);
//static ActivationKeypad keypad;

// Declare listeners
//static LockNotificationTask lockTask(transmitter, ledPanel);

// Declare periodic tasks
static PingTask pingTask(PING_PERIOD_SEC, transmitter, ledPanel);
//static VoltageNotificationTask voltageTask(VOLTAGE_PERIOD_SEC, transmitter);

//The setup function is called once at startup of the sketch
void setup()
{
//	RTC::begin();

	// Initialize power settings
	Power::twi_disable();
	Power::adc_disable();
//	Power::timer0_disable();
	Power::timer1_disable();
	Power::timer2_disable();
	// SPI shall be enabled when adding RF
//	Power::spi_disable();
	// USART shall be disabled on final module
	Power::usart0_disable();

	// Sleep modes by order of increasing consumption
	// Lowest consumption mode (works on Arduino, not tested yet on breadboard ATmega)
//	Power::set(SLEEP_MODE_PWR_DOWN);		// 0.36mA


//	Power::set(SLEEP_MODE_STANDBY);			// 0.84mA
//	Power::set(SLEEP_MODE_PWR_SAVE);		// 1.65mA
//	Power::set(SLEEP_MODE_EXT_STANDBY);		// 1.65mA
//	Power::set(SLEEP_MODE_ADC);				// 6.5 mA

	// Only this mode works when using serial output and alarm/RF?
	Power::set(SLEEP_MODE_IDLE);			// 15mA

	// Additional setup for transmitter goes here...

	// Start all tasks
//	pingTask.enable();
//	voltageTask.enable();

//	keypad.attachLockListener(&lockTask);

	// Start watchdog and keypad
	RTC::begin();
	Watchdog::begin(64, Watchdog::push_timeout_events);
	scheduler.begin();
//	keypad.begin();
	pingTask.enable();
}

// The loop function is called in an endless loop
void loop()
{
	//TODO not sure we really need Watchdog::await here, normally, Event::queue.await should be OK!
	Watchdog::await();
	Event event;
//	Event::queue.await(&event);
	while (Event::queue.dequeue(&event))
		event.dispatch();
}
