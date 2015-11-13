/*
 * File:   XTEATest.h
 * Author: Jean-François
 *
 * Created on 12 nov. 2015, 21:28:07
 */

#ifndef XTEATEST_H
#define	XTEATEST_H

#include <cppunit/extensions/HelperMacros.h>
#include "../Cipher.h"

class XTEATest : public CPPUNIT_NS::TestFixture {
	CPPUNIT_TEST_SUITE(XTEATest);

	CPPUNIT_TEST(testCipher);
	CPPUNIT_TEST(testDecipher);

	CPPUNIT_TEST_SUITE_END();

public:
	XTEATest();
	virtual ~XTEATest();
	void setUp();
	void tearDown();

private:
	void testCipher();
	void testDecipher();
	
	XTEA cipher;
};

#endif	/* XTEATEST_H */

