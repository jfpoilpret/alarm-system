/*
 * VoltageNotificationTask.hh
 *
 *  Created on: 21 janv. 2015
 *      Author: Jean-François
 */

#ifndef VOLTAGENOTIFICATIONTASK_HH_
#define VOLTAGENOTIFICATIONTASK_HH_

#include <Cosa/AnalogPin.hh>

#include "WDTAlarm.hh"
#include "ActivationNetwork.hh"
#include "LedPanel.hh"

class VoltageNotificationTask: public WDTAlarm
{
public:
	VoltageNotificationTask(uint32_t period, ActivationTransmitter& transmitter)
		:	WDTAlarm(period),
		 	_transmitter(transmitter) {}

	virtual void run()
	{
		// Get current voltage level
		uint16_t bandgap = AnalogPin::bandgap();

		// Send it to server
		_transmitter.sendVoltageLevel(bandgap);
	}

private:
	ActivationTransmitter& _transmitter;
};

#endif /* VOLTAGENOTIFICATIONTASK_HH_ */
