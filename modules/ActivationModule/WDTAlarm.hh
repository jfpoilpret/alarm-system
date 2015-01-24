/*
 * WDTAlarm.hh
 *
 *  Created on: 24 janv. 2015
 *      Author: Jean-François
 */

#ifndef WDTALARM_HH_
#define WDTALARM_HH_

#include <Cosa/Alarm.hh>

// Equivalent Alarm class except it does not need RTC but just relies only on Watchdog;
// Although that makes it a bit less accurate, it allows usage of all low power modes
// that are not possible when using RTC...
class WDTAlarm: public Alarm
{
public:
	WDTAlarm(uint32_t period = 0L)
		:Alarm(secsToWD(period)) {}

	class Scheduler: public Alarm::Scheduler
	{
	public:
		Scheduler()
		{
			set_period(WDT_PERIOD);
		}

	    virtual void run()
	    {
	    	Alarm::tick();
	    }
	};

private:
	static const uint32_t WDT_PERIOD = 1024;

	static uint32_t secsToWD(uint32_t seconds)
    {
		uint32_t ticks = seconds * 1000 / WDT_PERIOD;
		if ((seconds * 1000) % WDT_PERIOD)
			return ticks + 1;
		else
			return ticks;
	}
};

#endif /* WDTALARM_HH_ */
