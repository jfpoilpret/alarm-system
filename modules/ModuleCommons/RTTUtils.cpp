#include "RTTUtils.hh"

auto_RTT::auto_RTT()
{
	// Force our own yield() to use SLEEP_MODE_PWR_SAVE instead of SLEEP_MODE_PWR_DOWN,
	// otherwise RTC will not work during ::yield() calls, failing several timeout waiting loops
	_saveDelay = ::delay;
	_saveYield = ::yield;
	RTT::begin();
	RTT::micros(0);
	::yield = auto_RTT::yield;
}
		