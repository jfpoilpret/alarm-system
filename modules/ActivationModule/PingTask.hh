/*
 * PingTask.hh
 *
 *  Created on: 21 janv. 2015
 *      Author: Jean-François
 */

#ifndef PINGTASK_HH_
#define PINGTASK_HH_

#include "WDTAlarm.hh"

#include "ActivationNetwork.hh"
#include "LedPanel.hh"

class PingTask: public WDTAlarm
{
public:
	PingTask(uint32_t period, ActivationTransmitter& transmitter, LedPanel& ledPanel)
		:	WDTAlarm(period),
		 	_transmitter(transmitter),
		 	_ledPanel(ledPanel) {}

	virtual void run()
	{
		// Get lock status from server
		LockStatus status = _transmitter.pingServerAndGetLockStatus();
		// Dispatch status to LedPanel
		switch (status)
		{
		case UNKNOWN:
			_ledPanel.setLocked(false);
			_ledPanel.setUnlocked(false);
			break;

		case LOCKED:
			_ledPanel.setLocked(true);
			_ledPanel.setUnlocked(false);
			break;

		case UNLOCKED:
			_ledPanel.setLocked(false);
			_ledPanel.setUnlocked(true);
			break;
		}
	}

private:
	ActivationTransmitter& _transmitter;
	LedPanel& _ledPanel;
};

#endif /* PINGTASK_HH_ */
