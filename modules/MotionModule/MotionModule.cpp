#include <Cosa/InputPin.hh>
#include <Cosa/Watchdog.hh>
#include <stdint-gcc.h>

#include "Pins.hh"
#include "MotionNetwork.hh"

#include "CommonTasks.hh"
#include "MotionDetector.hh"

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
static const Board::DigitalPin CONFIG_PINS[] = {CONFIG_ID1, CONFIG_ID2, CONFIG_ID3, CONFIG_ID4};
static const uint8_t NUM_CONFIG_PINS = sizeof(CONFIG_PINS) / sizeof(Board::DigitalPin);

// Get the device ID from DIP switch pins
static uint8_t readConfigId()
{
	uint8_t id = 0;
	for (uint8_t i = 0; i < NUM_CONFIG_PINS; ++i)
	{
		InputPin::mode(CONFIG_PINS[i], InputPin::Mode::PULLUP_MODE);
		id <<= 1;
		if (!InputPin::read(CONFIG_PINS[i])) ++id;
		// Is it better to make it NORMAL_MODE? Some inputs are then left "open"!!!!
//		InputPin::mode(CONFIG_PINS[i], InputPin::Mode::NORMAL_MODE);
	}
	return id;
}
#else
static uint8_t readConfigId()
{
	return 0;
}
#endif

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

	// Start watchdog
	Watchdog::begin(WATCHDOG_PERIOD);
	// First wait 1 minute for PIR sensor to stabilize
	delay(PIR_STARTUP_TIME_MS);

	// Needed for Alarms to work properly
	Watchdog::Clock clock;

	// Declare sensors and actuators
	MotionTransmitter transmitter(SERVER_ID);
	MotionDetector detector(&transmitter);

	// Declare periodic tasks
	DefaultPingTask pingTask(&clock, PING_PERIOD_SEC, transmitter);
	VoltageNotificationTask voltageTask(&clock, VOLTAGE_PERIOD_SEC, transmitter);

	// Additional setup for transmitter goes here...
	transmitter.begin(NETWORK, MODULE_ID + readConfigId());

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
