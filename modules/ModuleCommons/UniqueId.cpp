#include <stdint-gcc.h>

#include "UniqueId.hh"

#define _input() *ddr &= reverse_mask
#define _output() *ddr |= mask
#define _is_clear() (*pin & mask)
#define _is_set() !(*pin & mask)
#define	_set() *port |= mask
#define	_clear() *port &= reverse_mask

void UniqueId::get_id(Board::DigitalPin pinNum, uint8_t id[UniqueId::ID_SIZE])
{
	volatile uint8_t* const pin = Pin::PIN(pinNum);
	volatile uint8_t* const ddr = pin + 1;
	volatile uint8_t* const port = ddr + 1;
	const uint8_t mask = Pin::MASK(pinNum);
	const uint8_t reverse_mask = ~mask;

	uint8_t retry = 4;
	uint8_t res = 0;
	do
	{
		_output();
		_set();
		_clear();
		DELAY(480);
		_set();
		_input();
		DELAY(70);
		res = _is_clear();
		DELAY(410);
	}
	while (retry-- && !res);
	uint8_t value = READ_ROM;
	_output();
	_set();
	for (uint8_t bit = 0; bit < CHARBITS; bit++)
	{
		_clear();
		if (value & 1)
		{
			DELAY(6);
			_set();
			DELAY(64);
		}
		else
		{
			DELAY(60);
			_set();
			DELAY(10);
		}
		value >>= 1;
	}
	_input();
	_clear();
	
	uint8_t size = ID_SIZE;
	while (size--)
	{
		uint8_t res = 0;
		for (uint8_t bit = 0; bit < CHARBITS; bit++)
		{
			_output();
			_set();
			_clear();
			DELAY(6);
			_input();
			DELAY(9);
			res >>= 1;
			if (_is_set())
				res |= 0x80;
			DELAY(55);
		}
		*id++ = res;
	}
}
