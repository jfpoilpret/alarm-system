#ifndef AUTO_RTT_HH_
#define AUTO_RTT_HH_

#include <Cosa/RTT.hh>

// This class is used to automatically enable/disable RTC clock for programs where we need it sometimes
// but don't want it working permanently (in order to benefit from lower power levels that are normally
// not possible when using RTC all the time)
class auto_RTT
{
public:
	auto_RTT()
	{
		// Force our own yield() to use SLEEP_MODE_PWR_SAVE instead of SLEEP_MODE_PWR_DOWN,
		// otherwise RTC will not work during ::yield() calls, failing several timeout waiting loops
		_saveDelay = ::delay;
		_saveYield = ::yield;
		RTT::begin();
		RTT::micros(0);
		::yield = auto_RTT::yield;
	}

	~auto_RTT()
		__attribute__((always_inline))
	{
		RTT::end();
		::yield = _saveYield;
		::delay = _saveDelay;
	}

private:
	static void yield()
	{
		// As timer2 is used, the best sleep mode we can use is SLEEP_MODE_PWR_SAVE
		// If another timer was used instead, we would have to use SLEEP_MODE_IDLE instead
		Power::sleep(SLEEP_MODE_PWR_SAVE);
//		Power::sleep(SLEEP_MODE_IDLE);
	}

	void (*_saveYield)();
	void (*_saveDelay)(uint32_t);
};

#endif /* AUTO_RTT_HH_ */
