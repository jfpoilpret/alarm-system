/*
 * RTCAdapter.hh
 *
 *  Created on: 24 janv. 2015
 *      Author: Jean-François
 */

#ifndef RTCADAPTER_HH_
#define RTCADAPTER_HH_

#include <Cosa/RTC.hh>

#include "DebugLed.hh"

//TODO rename to auto_RTC
//TODO refactor in 2 utility classes one for RTC enable, one for yield change
// This class is used to automatically enable/disable RTC clock for programs where we need it sometimes
// but don't want it working permanently (in order to benefit from lower power levels that are normally
// not possible when using RTC all the time)
class RTCAdapter
{
public:
	static void init()
	{
		// At first time it is called, RTC::begin() sets ::delay to RTC::delay
		// but we don't want it as default delay method, so restore the original method
		void (*saveDelay)(uint32_t) = ::delay;
		RTC::begin();
		RTC::end();
		::delay = saveDelay;
	}

	RTCAdapter()
	{
		// Force our own yield() to use SLEEP_IDLE_MODE instead of SLEEP_MODE_PWR_DOWN,
		// otherwise RTC will not work during ::yield() calls, failing several timeout waiting loops
		_saveYield = ::yield;
		::yield = RTCAdapter::yield;
		synchronized
		{
			// And enable interrupt on overflow
			TIMSK0 = _BV(TOIE0);
			// Reset the counter and clear interrupts
			TCNT0 = 0;
			TIFR0 = 0;
		}
		RTC::micros(0);
	}

	~RTCAdapter()
		__attribute__((always_inline))
	{
		// Disable interrupt on overflow
		synchronized
		{
			// And enable interrupt on overflow
			TIMSK0 = 0;
		}
		::yield = _saveYield;
	}

private:
	static void yield()
	{
//		debug(3);
		Power::sleep(SLEEP_MODE_IDLE);
	}

	void (*_saveYield)();
};

#endif /* RTCADAPTER_HH_ */
