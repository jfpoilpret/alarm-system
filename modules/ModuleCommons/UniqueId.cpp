#include <stdint-gcc.h>

#include "UniqueId.hh"

UniqueId::UniqueId(Board::DigitalPin pin):
	m_pin(Pin::PIN(pin)), m_ddr(m_pin+1), m_port(m_pin+2), m_mask(Pin::MASK(pin)), m_reverse_mask(~m_mask) {}

void UniqueId::get_id(uint8_t id[UniqueId::ID_SIZE])
{
	cli();
	_reset();
	_write_byte(READ_ROM);
	_read(id, ID_SIZE);
	sei();
}

void UniqueId::_reset()
{
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
}

void UniqueId::_write_byte(uint8_t value)
{
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
}

uint8_t UniqueId::_read_byte()
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
	return res;
}

void UniqueId::_read(void* buf, uint8_t size)
{
	uint8_t* bp = (uint8_t*) buf;
	while (size--) *bp++ = _read_byte();
}
