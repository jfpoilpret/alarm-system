#ifndef LOWPOWERLEDBLINKER_HH_
#define LOWPOWERLEDBLINKER_HH_

#include <util/delay.h>
#include <Cosa/OutputPin.hh>

//TODO Led blinker with low current consumption:
// - uses WDT to blink LED
class LowPowerLedBlinker: private Link, private OutputPin
{
public:
	LowPowerLedBlinker(	const Board::DigitalPin pin,
						uint8_t initial = 0,
						uint16_t on_period_ms = TIME_ON_MS,
						uint16_t off_period_ms = TIME_OFF_MS)
		:	OutputPin(pin), _state(0)
	{
		_set(initial);
		Watchdog::attach(this, period);
	}

	void on()
		__attribute__((always_inline))
	{
		set(true);
	}

	void off()
		__attribute__((always_inline))
	{
		set(false);
	}

	void set(bool value)
		__attribute__((always_inline))
	{
		if (_state != value) _set(value);
	}

    virtual void on_event(uint8_t type, uint16_t value);

private:
	void _set(bool value);

	// if REFRESH_MS > 32, then the LED will blink instead of appearing
	// NB: that default value may be too long, depending on MCU activity...
	static const uint16_t PERIOD_MS = 2048;
	static const uint16_t TIME_ON_MS = 8;
	static const uint16_t TIME_OFF_MS = PERIOD_MS - TIME_ON_MS;
	static const uint16_t REFRESH_MS = 32;
	static const uint16_t DURATION_US = 500;

    uint8_t _state;
    uint8_t _counter;
    uint8_t _max_counter;
    uint16_t _time_on;
    uint16_t _time_off;
};

void LowPowerLedBlinker::on_event(uint8_t type, uint16_t value)
{
	UNUSED(value);
	if (type == Event::TIMEOUT_TYPE && _state)
	{
		OutputPin::on();
		_delay_us(DURATION_US);
//		_delay_ms(DURATION_MS);
		OutputPin::off();
	}
}

void LowPowerLedBlinker::_set(bool value)
{
	_state = value;
	if (!_state)
		OutputPin::off();
}

#endif /* LOWPOWERLEDBLINKER_HH_ */
