#ifndef UNIQUEID_HH
#define	UNIQUEID_HH

#include <Cosa/Pin.hh>

class UniqueId
{
public:
	static const size_t ID_SIZE = 8;

	UniqueId(Board::DigitalPin pin);
	void get_id(uint8_t id[ID_SIZE]);
	
protected:
	static const uint8_t READ_ROM = 0x33;

	void _input()
		__attribute__((always_inline))
	{
		*m_ddr &= m_reverse_mask;
	}
	void _output()
		__attribute__((always_inline))
	{
		*m_ddr |= m_mask;
	}
	bool _is_clear() const
		__attribute__((always_inline))
	{
		return (*m_pin & m_mask);
	}
	bool _is_set() const
		__attribute__((always_inline))
	{
		return !(*m_pin & m_mask);
	}
	void _set() const
		__attribute__((always_inline))
	{
		*m_port |= m_mask;
	}
	void _clear() const
		__attribute__((always_inline))
	{
		*m_port &= m_reverse_mask;
	}
	
	void _reset();
	uint8_t _read_byte();
	void _read(void* buf, uint8_t size);
	void _write_byte(uint8_t value);

private:
	volatile uint8_t* const m_pin;
	volatile uint8_t* const m_ddr;
	volatile uint8_t* const m_port;
	const uint8_t m_mask;
	const uint8_t m_reverse_mask;
};

#endif	/* UNIQUEID_HH */

