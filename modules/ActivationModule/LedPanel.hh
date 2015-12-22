/*
 * LedPanel.hh
 *
 *  Created on: 21 janv. 2015
 *      Author: Jean-Fran�ois
 */

#ifndef LEDPANEL_HH_
#define LEDPANEL_HH_

#include <Cosa/Periodic.hh>
#include "Pins.hh"

class LedPanel
{
public:
	LedPanel(Periodic& timer)
		:_locked(timer, LED_LOCKED, 0), _unlocked(timer, LED_UNLOCKED, 0) {}

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
