/*
 * RTCAdapter.hh
 *
 *  Created on: 24 janv. 2015
 *      Author: Jean-François
 */

#ifndef RTCADAPTER_HH_
#define RTCADAPTER_HH_

#include <Cosa/RTC.hh>

// This class is used to automatically enable/disable RTC clock for programs where we need it sometimes
// but don't want it working permanently (in order to benefit from lower power levels that are normally
// not possible when using RTC all the time)
class RTCAdapter
{
public:
	RTCAdapter()
	{
		if (!RTC::begin())
		{
			synchronized
			{
				// And enable interrupt on overflow
				TIMSK0 = _BV(TOIE0);
				// Reset the counter and clear interrupts
				TCNT0 = 0;
				TIFR0 = 0;
			}
		}
	}

	~RTCAdapter()
		__attribute__((always_inline))
	{
		// Disable interrupt on overflow
		RTC::end();
	}
};

#endif /* RTCADAPTER_HH_ */
