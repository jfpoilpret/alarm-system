/*
 * File:   XTEATest.cpp
 * Author: Jean-François
 *
 * Created on 12 nov. 2015, 21:28:07
 */

#include <stdint.h>
#include <cstring>
#include <time.h>
#include <iostream>
#include "XTEATest.h"

static timespec current_time() {
	timespec time;
	clock_gettime(CLOCK_REALTIME, &time);
	return time;
}

static uint64_t us_since(const timespec& since) {
	timespec now = current_time();
	return (now.tv_sec - since.tv_sec) * 1000000 + (now.tv_nsec - since.tv_nsec) / 1000;
}

CPPUNIT_TEST_SUITE_REGISTRATION(XTEATest);

union Message {
	uint32_t code[2];
	char content[8];
};

XTEATest::XTEATest() {
}

XTEATest::~XTEATest() {
}

void XTEATest::setUp() {
	cipher = XTEA();
	const uint8_t key[XTEA::KEY_SIZE] = {
		0x00,
		0x11,
		0x22,
		0x33,
		0x44,
		0x55,
		0x66,
		0x77,
		0x88,
		0x99,
		0xAA,
		0xBB,
		0xCC,
		0xDD,
		0xEE,
		0xFF
	};
	timespec now = current_time();
	cipher.set_key(key);
	uint64_t duration = us_since(now);
	std::cout << "XTEA::set_key() lasted " << std::dec << duration << "us" << std::endl;
}

void XTEATest::tearDown() {
}

void XTEATest::testCipher() {
	Message msg;
	strcpy(msg.content, "1234567");
	
	cipher.encipher(msg.code);
	CPPUNIT_ASSERT(strcmp(msg.content, "1234567") != 0);
	
	timespec now = current_time();
	cipher.decipher(msg.code);
	uint64_t duration = us_since(now);
	std::cout << "XTEA::decipher() lasted " << std::dec << duration << "us" << std::endl;
	CPPUNIT_ASSERT(strcmp(msg.content, "1234567") == 0);
}
