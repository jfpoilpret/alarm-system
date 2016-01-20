#include <Cosa/InputPin.hh>
#include <Cosa/Watchdog.hh>
#include <stdint-gcc.h>

#include "Pins.hh"
#include "MotionNetwork.hh"

#include "CommonTasks.hh"
#include "PingTask.hh"
#include "MotionDetector.hh"
#include "UniqueId.hh"

//TODO Externalize these constants?
static const uint16_t NETWORK = 0xC05A;
static const uint8_t SERVER_ID = 0x01;
static const uint8_t MODULE_ID = 0x20;

static const uint32_t PING_PERIOD_SEC = 5;
static const uint32_t VOLTAGE_PERIOD_SEC = 60;
//static const uint32_t VOLTAGE_PERIOD_SEC = 3600;
static const uint32_t PIR_STARTUP_TIME_MS = 60000L;

// Watchdog period must be the minimum of periods required by all watchdog timer users:
// - Alarm			1024ms
// - Event handling	16ms
static const uint16_t WATCHDOG_PERIOD = 16;

#ifdef BOARD_ATTINYX4
// Get the device ID from DIP switch pins
static void readConfigId()
{
	uint8_t id[UniqueId::ID_SIZE];
	UniqueId::get_id(TEMP_SENSOR_PIN, id);
}
#else
static void readConfigId()
{
	uint8_t id[UniqueId::ID_SIZE];
	UniqueId::get_id(TEMP_SENSOR_PIN, id);
}
#endif

int main()
{
	// Disable analog comparator
	ACSR = _BV(ACD);
	// Disable all modules but ADC (required for bandgap reading)
	Power::all_disable();
	Power::adc_enable();
	// Read device ID from OWI temperature sensor
	readConfigId();
	// Allow interrupts from here
	sei();
	
	// Start watchdog
	Watchdog::begin(WATCHDOG_PERIOD);
	// First wait 1 minute for PIR sensor to stabilize
	delay(PIR_STARTUP_TIME_MS);

	// Needed for Alarms to work properly
	Watchdog::Clock clock;

	// Declare sensors, actuators and periodic tasks
	MotionTransmitter transmitter(SERVER_ID);
	MotionDetector detector(&transmitter);

	PingTask pingTask(&clock, PING_PERIOD_SEC, transmitter);
	VoltageNotificationTask voltageTask(&clock, VOLTAGE_PERIOD_SEC, transmitter);

	// Additional setup for transmitter goes here...
	transmitter.begin(NETWORK, MODULE_ID);
//	transmitter.begin(NETWORK, MODULE_ID + readConfigId());

	// Start all tasks
	// However, do note that detection module is not really started until PinChangeInterrupt has begun
	// which will occur only if alarm is active (i.e. status is LOCKED)
	pingTask.start();
	voltageTask.start();

	while (true)
	{
		// Lowest consumption mode
		Power::set(SLEEP_MODE_PWR_DOWN);		// 0.36mA
		Watchdog::await();
		// Only this mode works when using serial output and full-time RTC
		Power::set(SLEEP_MODE_IDLE);			// 15mA

		Event event;
		while (Event::queue.dequeue(&event))
			event.dispatch();
	}
}
