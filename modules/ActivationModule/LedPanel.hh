/*
 * LedPanel.hh
 *
 *  Created on: 21 janv. 2015
 *      Author: Jean-François
 */

#ifndef LEDPANEL_HH_
#define LEDPANEL_HH_

#include "Pins.hh"

class LedPanel
{
public:
	LedPanel()
		:_locked(LED_LOCKED, 0), _unlocked(LED_UNLOCKED, 0) {}

	void updateStatus(bool lock)
	{
		_locked.set(lock);
		_unlocked.set(!lock);
	}

private:
	LowPowerLed _locked;
	LowPowerLed _unlocked;
};



#endif /* LEDPANEL_HH_ */
