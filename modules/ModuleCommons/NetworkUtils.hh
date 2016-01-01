#ifndef NETWORKUTILS_HH_
#define NETWORKUTILS_HH_

#include <NRF24L01P.h>
#ifndef NO_CIPHER
#include "Cipher.hh"
#endif

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
#ifndef NO_CIPHER
	uint8_t key[XTEA::KEY_SIZE];
#endif
};

union RxPayload
{
	RxPingServer pingServer;
};

class AbstractTransmitter
{
public:
    void address(int16_t net, uint8_t dev);
	// Register the activation module to the alarm center, get new cipher key,
	// get current alarm status (locked/unlocked).
	// Normally this method is called every 5 seconds.
	LockStatus pingServerAndGetLockStatus();
	// Notify alarm center about current voltage level (in mV).
	// This method is typically called once per hour or so
	void sendVoltageLevel(uint16_t level);

private:
	NRF24L01P _nrf;
	
protected:
	AbstractTransmitter(uint8_t server, 
		Board::DigitalPin csn, Board::DigitalPin ce, Board::ExternalInterruptPin irq);

	int recv(uint8_t& src, uint8_t& port, void* buf, size_t count, uint32_t ms = 0L);
	int send(uint8_t dest, uint8_t port, const void* buf, size_t len);

//	static const uint8_t RECV_TIMEOUT_MS = 5;
	static const uint8_t RECV_TIMEOUT_MS = 10;
	const uint8_t _server;
#ifndef NO_CIPHER
	XTEA _cipher;
#endif
	friend class auto_standby;
};

class auto_standby
{
public:
	auto_standby(AbstractTransmitter& transmitter);
	~auto_standby() { _rf.standby(); }
private:
	NRF24L01P& _rf;
};

#endif /* NETWORKUTILS_HH_ */
