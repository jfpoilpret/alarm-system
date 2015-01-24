#include <Cosa/RTC.hh>
#include <Cosa/Trace.hh>
#include <Cosa/IOStream/Driver/UART.hh>
#include <Cosa/Wireless/Driver/NRF24L01P.hh>

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

//The setup function is called once at startup of the sketch
void setup()
{
	RTC::begin();
	uart.begin(57600);
	trace.begin(&uart, PSTR("Server started."));
	rf.begin();
}

static bool locked = true;

// The loop function is called in an endless loop
void loop()
{
	uint16_t buffer[SIZE];
	uint8_t source = 0xFF;
	uint8_t type = 0xFF;
	int size = rf.recv(source, type, buffer, sizeof(buffer));
	trace << ":recv source=" << hex << source << ", type=" << hex << type << ", size=" << size << endl;
	if (size < 0) return;

	uint16_t& level = *((uint16_t*) buffer);
	char* input = (char*) buffer;
	int rsize = 0;
	switch (type)
	{
	case PING_SERVER:
		trace << "PING_SERVER" << endl;
		rsize = rf.send(source, PING_SERVER, &locked, sizeof(locked));
//		locked = !locked;
		break;

	case VOLTAGE_LEVEL:
		trace << "VOLTAGE_LEVEL level=" << level << endl;
		break;

	case LOCK_CODE:
	case UNLOCK_CODE:
		trace << (type == UNLOCK_CODE ? "UN": "") << "LOCK_CODE input=" << input << endl;
		if (strcmp(input, CODE) == 0)
			locked = (type == LOCK_CODE);
		rsize = rf.send(source, type, &locked, sizeof(locked));
		break;

	default:
		trace << "UNKNOWN type!" << endl;
		break;
	}
	trace << ":send size=" << rsize << endl;
}
