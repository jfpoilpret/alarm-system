#include <Cosa/Alarm.hh>
#include <Cosa/AnalogPin.hh>
#include <Cosa/InputPin.hh>
#include <Cosa/PinChangeInterrupt.hh>
#include <Cosa/RTT.hh>
#include <Cosa/Watchdog.hh>
#include <stdint-gcc.h>
#include "NRF24L01P.h"

//PINS
static const Board::DigitalPin NRF_POWER			= Board::D8;
static const Board::DigitalPin NRF_CSN				= Board::D7;
static const Board::DigitalPin NRF_CE				= Board::D3;
static const Board::ExternalInterruptPin NRF_IRQ	= Board::EXT0;
static const Board::DigitalPin PIR_POWER			= Board::D2;
static const Board::InterruptPin PIR_MOTION_INT		= Board::PCI1;

// NETWORK ADDRESSES
static const uint16_t NETWORK = 0xC05A;
static const uint8_t SERVER_ID = 0x01;
static const uint8_t MODULE_ID = 0x20;

// TIMING CONSTANTS
static const uint32_t STARTUP_LED_TIME_MS = 500;

static const uint16_t WATCHDOG_PERIOD = 1024;

// PROTOCOL
enum LockStatus
{
	UNKNOWN,
	LOCKED,
	UNLOCKED,
};

enum MessageType
{
	// General messages, used by all sensors
	PING_SERVER = 0x01,
	VOLTAGE_LEVEL = 0x02,

	// Messages specific to the activation module
	LOCK_CODE = 0x10,
	UNLOCK_CODE = 0x11,

	// Messages specific to the motion detection module
	MOTION_DETECTED = 0x20
			
	// Other messages will go there

} __attribute__((packed));

struct RxPingServer
{
	bool locked;
};

union RxPayload
{
	RxPingServer pingServer;
};

class PIRActivator: public Alarm
{
public:
	PIRActivator(::Clock* clock):Alarm(clock, PIR_STARTUP_TIME_SEC) {}
	
	void restart()
	{
		Alarm::expire_at(Alarm::time() + PIR_STARTUP_TIME_SEC);
		Alarm::start();
	}

	virtual void run()
	{
		PinChangeInterrupt::begin();
		Alarm::stop();
	}
	
private:
	static const uint32_t PIR_STARTUP_TIME_SEC = 60;
};

class PingTask: public Alarm
{
public:
	PingTask(::Clock* clock, NRF24L01P& nrf, PIRActivator& pirActivator)
	:	Alarm(clock, PING_PERIOD_SEC), 
		_nrf(nrf), _pirActivator(pirActivator), _pir_power(PIR_POWER, 1), _status(UNKNOWN), 
		_ping_count(0), _pings_per_voltage(VOLTAGE_PERIOD_SEC / PING_PERIOD_SEC) {}
	
	//TODO refactor sendVoltageLevel and pingServerAndGetLockStatus into one method
	LockStatus sendVoltageLevel(uint16_t level)
	{
		_nrf.send(VOLTAGE_LEVEL, &level, sizeof(level));
		return UNKNOWN;
	}
	
	LockStatus pingServerAndGetLockStatus()
	{
		LockStatus status = UNKNOWN;
		// Ping server
		if (_nrf.send(PING_SERVER, 0, 0) >= 0)
		{
			// Wait for acknowledge with lock status and optional cipher key
			RxPingServer response;
			int size = _nrf.recv(PING_SERVER, &response, sizeof(response));
			if (size > 0)
				status = response.locked ? LOCKED : UNLOCKED;
		}
		return status;
	}
	
	virtual void run()
	{
		LockStatus status = UNKNOWN;
		if (++_ping_count == _pings_per_voltage)
		{
			_ping_count = 0;
			// Get current voltage level
			uint16_t bandgap = AnalogPin::bandgap();
			// Send it to server
			status = sendVoltageLevel(bandgap);
		}
		else
		{
			// Get lock status from server
			status = pingServerAndGetLockStatus();
		}
		if (_status != status && status != UNKNOWN)
		{
			_status = status;
			bool locked = (_status == LOCKED);
			if (locked)
			{
				// start PIR and delay until PIR ready before lsitening to PIR interrupts
				_pirActivator.restart();
			}
			else
			{
				// stop PIR & stop listening to PIR interrupts
				_pirActivator.stop();
				PinChangeInterrupt::end();
			}
			_pir_power.set(!locked);
		}
	}

private:
	static const uint32_t PING_PERIOD_SEC = 10;
	static const uint32_t VOLTAGE_PERIOD_SEC = 60;

	NRF24L01P& _nrf;
	PIRActivator& _pirActivator;
	OutputPin _pir_power;
	LockStatus _status;
	uint16_t _ping_count;
	const uint16_t _pings_per_voltage;
};

class PIRDetector: public PinChangeInterrupt, public Event::Handler
{
public:
	static const uint8_t MOTION_EVENT = Event::USER_TYPE + 1;
	
	PIRDetector(NRF24L01P& nrf)
		:	PinChangeInterrupt(PIR_MOTION_INT, PinChangeInterrupt::ON_RISING_MODE),
			_nrf(nrf) {}
	virtual void on_interrupt(uint16_t arg)
	{
		// Do nothing yet
		UNUSED(arg);
		Event::push(MOTION_EVENT, this, this);
	}
	
	virtual void on_event(uint8_t type, uint16_t value)
	{
		UNUSED(type);
		UNUSED(value);
		_nrf.send(MOTION_DETECTED, 0, 0);
	}
	
private:
	NRF24L01P& _nrf;
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

	// Start watchdog
	Watchdog::begin(WATCHDOG_PERIOD);
	Power::set(SLEEP_MODE_PWR_DOWN);		// 5uA
	
	// DEBUG First light startup LED for 5 seconds
	//TODO if commenting out this code makes it work better (no high currents at start) then
	// perform a new check but with first forcing 0 to Transistor output
	{
		OutputPin led = Board::D0;
		led.on();
		delay(STARTUP_LED_TIME_MS);
		led.off();
	}

	// Needed for Alarms to work properly
	Watchdog::Clock clock;

	NRF24L01P transmitter = NRF24L01P(SERVER_ID, NRF_POWER, NRF_CSN, NRF_CE, NRF_IRQ);
	transmitter.address(NETWORK, MODULE_ID);
	// TODO PIRActivator could be a member of PingTask instead (less arguments))
	PIRActivator pirActivator(&clock);
	PingTask pingTask(&clock, transmitter, pirActivator);
	
	PIRDetector detector(transmitter);
	detector.enable();

	// Start all tasks
	// However, do note that detection module is not really started until PinChangeInterrupt has begun
	// which will occur only if alarm is active (i.e. status is LOCKED)
	pingTask.start();
//	PinChangeInterrupt::begin();

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
			//TODO Not sure the following is REALLY necessary...
//			RTT::millis(0);
			// Start NRF
			transmitter.begin();
			
			Event event;
			while (Event::queue.dequeue(&event))
				event.dispatch();
			
			// Stop NRF
			transmitter.end();
			// Stop using RTT and restore Watchdog
			RTT::end();
			::delay = Watchdog::delay;
			// Lowest consumption mode
			Power::set(SLEEP_MODE_PWR_DOWN);		// 5uA
		}
	}
}
