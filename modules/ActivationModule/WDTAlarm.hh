/*
 * WDTAlarm.hh
 *
 *  Created on: 24 janv. 2015
 *      Author: Jean-François
 */

#ifndef WDTALARM_HH_
#define WDTALARM_HH_

#include <Cosa/Linkage.hh>
#include <Cosa/Watchdog.hh>

#include <Cosa/Alarm.hh>

//TODO equivalent of the Alarm class except it does not need RTC but just relies only on Watchdog;
// Although that makes it less accurate, it allows usage of lower power modes that are not possible
// when using RTC...
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


//class WDTAlarm: private Link
//{
//
//private:
//	static clock_t s_ticks;
//	static Head s_queue;
//	uint32_t m_when;
//	uint32_t m_period;
//};

#endif /* WDTALARM_HH_ */
