/* 
 * File:   main.cpp
 *
 * Main entry point of Alarm System central process to communicate to sensor devices through NRF24L01 chip.
 * This process is used to communicate with all devices and proxy all exchanges from/to the web system 
 * on Raspbery Pi (Python-based).
 */

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string.h>
#include "NRF24L01P.h"
#include "Cipher.h"

using namespace std;

const uint16_t NETWORK = 0xC05A;
const uint8_t SERVER_ID = 0x01;

const size_t MESSAGE_MAX_SIZE = NRF24L01P::PAYLOAD_MAX;

#pragma pack(1)

union ReceptionPayload {
	uint8_t raw[MESSAGE_MAX_SIZE];
	uint32_t crypted_code[2];
	char code[8];
	uint16_t voltage;
};

static void handle(NRF24L01P& nrf, uint8_t src, uint8_t port, ReceptionPayload& message, int count);

int main(int argc, char** argv) {
	cout << "Instantiate NRF24..." << endl;
	NRF24L01P nrf(NETWORK, SERVER_ID);
	cout << "NRF24 instance created." << endl;
	nrf.begin();
	cout << "NRF24 instance started." << endl;
	srand(time(0));
	while (true) {
		uint8_t src;
		uint8_t port;
		ReceptionPayload message;
		int count = nrf.recv(src, port, message.raw, MESSAGE_MAX_SIZE, 1000L);
		switch (count) {
			case EIO:
			case EINVAL:
			case EMSGSIZE:
				cout << "Got error " << dec <<count << endl;
				break;

			case ETIME:
				cout << "." << flush;
				break;
				
			default:
//				cout << "R" << hex << (uint16_t) port << "-" << dec << count << " " << flush;
				handle(nrf, src, port, message, count);
				break;
		}
		cout	<< " TX " << dec << nrf.get_trans() << ":" << nrf.get_retrans() 
				<< ":" << nrf.get_drops() << ":" << nrf.get_missing_irq() << endl;
	}
	return 0;
}

static void check_send(int count) {
	if (count < 0) {
		cout << " TX " << dec << count << " " << flush;
	}
}

static void handle(NRF24L01P& nrf, uint8_t src, uint8_t port, ReceptionPayload& message, int count) {
	static bool first = true;
	static XTEA cipher;
	static uint8_t lock = 0;
	switch(port) {
		case 0x01:
			// ping: randomly return a new XTEA cipher key
			if (first or (rand() % 100 < 5)) {
				first = false;
				uint8_t payload[XTEA::KEY_SIZE + 1];
				payload[0] = lock;
				XTEA::generate_key(&payload[1]);
				cipher.set_key(&payload[1]);
				check_send(nrf.send(src, port, payload, sizeof payload));
				cout << "PK " << endl;
			} else {
				check_send(nrf.send(src, port, &lock, sizeof lock));
				cout << "P " << endl;
			}
			break;
			
		case 0x02:
			// voltage: just display voltage
			cout << "V:" << dec << message.voltage << " mV" << endl;
			break;
			
		case 0x10:
		case 0x11:
			// decipher code first
			cipher.decipher(message.crypted_code);
			cout << (port == 0x10 ? "L:" : "U:") << message.code << endl;
			if (strcmp(message.code, "123456") == 0)
				lock = (port == 0x10 ? 1 : 0);
			check_send(nrf.send(src, port, &lock, sizeof lock));
			break;
	}
}
