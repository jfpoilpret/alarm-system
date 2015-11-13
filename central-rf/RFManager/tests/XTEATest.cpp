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

const char* CLEAR_CODE = "1234567";
const uint8_t CRYPTED_CODE[] = {
	0x9b,
	0xef,
	0x80,
	0x5a,
	0xbd,
	0xec,
	0x0f,
	0xd1
};

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
	strcpy(msg.content, CLEAR_CODE);
	
	timespec now = current_time();
	cipher.encipher(msg.code);
	uint64_t duration = us_since(now);
	std::cout << "XTEA::encipher('" << CLEAR_CODE << "') = ";
	for (uint8_t i = 0; i < 8; i++)
		std::cout << std::hex << (uint16_t) msg.content[i] << ' ';
	std::cout << " lasted " << std::dec << duration << "us" << std::endl;
	
	CPPUNIT_ASSERT(memcmp(msg.code, CRYPTED_CODE, sizeof CRYPTED_CODE) == 0);
}

void XTEATest::testDecipher() {
	Message msg;
	memcpy(msg.code, CRYPTED_CODE, sizeof CRYPTED_CODE);
	
	timespec now = current_time();
	cipher.decipher(msg.code);
	uint64_t duration = us_since(now);
	std::cout << "XTEA::decipher() lasted " << std::dec << duration << "us" << std::endl;
	CPPUNIT_ASSERT(strcmp(msg.content, CLEAR_CODE) == 0);
}
