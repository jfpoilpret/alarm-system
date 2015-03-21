#ifndef LOWPOWERLED_HH_
#define LOWPOWERLED_HH_

#include <util/delay.h>
#include <Cosa/OutputPin.hh>

class LowPowerLed: private Link, private OutputPin
{
public:
	LowPowerLed(const Board::DigitalPin pin,
				uint8_t initial = 0,
				uint16_t period = REFRESH_MS)
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
	static const uint16_t REFRESH_MS = 32;
	static const uint16_t DURATION_US = 500;

    uint8_t _state;
};

void LowPowerLed::on_event(uint8_t type, uint16_t value)
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

void LowPowerLed::_set(bool value)
{
	_state = value;
	if (!_state)
		OutputPin::off();
}

#endif /* LOWPOWERLED_HH_ */
