#ifndef AUTO_RTT_HH_
#define AUTO_RTT_HH_

#include <Cosa/RTT.hh>
#include <Cosa/Watchdog.hh>

// This class is used to automatically enable/disable RTC clock for programs where we need it sometimes
// but don't want it working permanently (in order to benefit from lower power levels that are normally
// not possible when using RTC all the time)
class auto_RTT
{
public:
	auto_RTT()
	{
		RTT::begin();
		RTT::micros(0);
	}

	~auto_RTT()
		__attribute__((always_inline))
	{
		RTT::end();
		// Restore Watchdog delay function (because RTT::end() does not do it, although it should)
		::delay = Watchdog::delay;
	}
};

#endif /* AUTO_RTT_HH_ */
