#ifndef LEDPANEL_HH_
#define LEDPANEL_HH_

#include <Cosa/Periodic.hh>
#include "LowPowerLed.hh"
#include "Pins.hh"

class LedPanel
{
public:
	LedPanel(Job::Scheduler* scheduler)
		:_locked(LED_LOCKED, scheduler), _unlocked(LED_UNLOCKED, scheduler) {}

	void setLocked(bool on)
	{
		_locked.set(on);
	}
	void setUnlocked(bool on)
	{
		_unlocked.set(on);
	}

private:
	LowPowerLed _locked;
	LowPowerLed _unlocked;
};

#endif /* LEDPANEL_HH_ */
