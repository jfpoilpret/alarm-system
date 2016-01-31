#ifndef UNIQUEID_HH
#define	UNIQUEID_HH

#include <Cosa/Pin.hh>

class UniqueId
{
public:
	static const size_t ID_SIZE = 8;

	static void get_id(Board::DigitalPin pin, uint8_t id[ID_SIZE]) __attribute__((OS_main));
	
private:
	static const uint8_t READ_ROM = 0x33;
};

#endif	/* UNIQUEID_HH */

