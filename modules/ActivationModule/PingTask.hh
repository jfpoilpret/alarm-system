/*
 * PingTask.hh
 *
 *  Created on: 21 janv. 2015
 *      Author: Jean-François
 */

#ifndef PINGTASK_HH_
#define PINGTASK_HH_

#include <Cosa/Alarm.hh>

#include "ActivationNetwork.hh"
#include "LedPanel.hh"

class PingTask: public Alarm
{
public:
	PingTask(uint32_t period, ActivationTransmitter& transmitter, LedPanel& ledPanel)
		:	Alarm(period),
		 	_transmitter(transmitter),
		 	_ledPanel(ledPanel) {}

	virtual void run()
	{
		// Get lock status from server
		bool status = _transmitter.pingServerAndGetLockStatus();
		// Dispatch status to LedPanel
		_ledPanel.updateStatus(status);
	}

private:
	ActivationTransmitter& _transmitter;
	LedPanel& _ledPanel;
};

#endif /* PINGTASK_HH_ */
