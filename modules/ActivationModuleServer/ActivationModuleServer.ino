#include <Cosa/RTC.hh>
#include <Cosa/Trace.hh>
#include <Cosa/IOStream/Driver/UART.hh>
#include <Cosa/Wireless/Driver/NRF24L01P.hh>

#include "Cipher.hh"

const char* CODE = "123456";

const uint16_t NETWORK = 0xC05A;
const uint8_t SERVER_ID = 0x01;

const size_t SIZE = 16;

static NRF24L01P rf(NETWORK, SERVER_ID);

enum MessageType
{
	// General messages, used by all sensors
	PING_SERVER = 0x01,
	VOLTAGE_LEVEL = 0x02,

	// Messages specific to the activation module
	LOCK_CODE = 0x10,
	UNLOCK_CODE = 0x11,

	// Other messages will go there

} __attribute__((packed));

struct RxPingServer
{
	bool locked;
	uint8_t key[XTEA::KEY_SIZE];
};

//The setup function is called once at startup of the sketch
void setup()
{
	RTC::begin();
	uart.begin(57600);
	trace.begin(&uart, PSTR("Server started."));
	rf.begin();
}

static XTEA cipher;
static clock_t lastKeyGenTime;

static bool locked = true;

// The loop function is called in an endless loop
void loop()
{
	uint16_t buffer[SIZE];
	uint8_t source = 0xFF;
	uint8_t type = 0xFF;
	int size = rf.recv(source, type, buffer, sizeof(buffer));
//	trace << ":recv source=" << hex << source << ", type=" << hex << type << ", size=" << size << endl;
	if (size < 0) return;

	uint16_t& level = *((uint16_t*) buffer);
	switch (type)
	{
	case PING_SERVER:
		trace << "PING_SERVER" << endl;
		if (RTC::seconds() > lastKeyGenTime)
		{
			RxPingServer payload;
			cipher.generate_key(payload.key);
			cipher.set_key(payload.key);
			payload.locked = locked;
			trace	<< "New key generated: " << hex
					<< payload.key[0] << payload.key[1] << payload.key[2] << payload.key[3]
					<< payload.key[4] << payload.key[5] << payload.key[6] << payload.key[7] << endl;
			rf.send(source, PING_SERVER, &payload, sizeof(payload));
			lastKeyGenTime = RTC::seconds() + 120;//TODO avoid hardcoded constant!!!
		}
		else
		{
			rf.send(source, PING_SERVER, &locked, sizeof(locked));
		}
		break;

	case VOLTAGE_LEVEL:
		trace << "VOLTAGE_LEVEL level=" << level << endl;
		break;

	case LOCK_CODE:
	case UNLOCK_CODE:
	{
		// Decipher received code
		cipher.decipher((uint32_t*) buffer);
		char* input = (char*) buffer;
		trace << (type == UNLOCK_CODE ? "UN": "") << "LOCK_CODE input=" << input << endl;
		if (strcmp(input, CODE) == 0)
			locked = (type == LOCK_CODE);
		rf.send(source, type, &locked, sizeof(locked));
		break;
	}

	default:
		trace << "UNKNOWN type! " << type << endl;
		break;
	}
//	trace << ":send size=" << rsize << endl;
}
