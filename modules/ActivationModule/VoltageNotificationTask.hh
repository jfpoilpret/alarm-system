/*
 * VoltageNotificationTask.hh
 *
 *  Created on: 21 janv. 2015
 *      Author: Jean-Fran�ois
 */

#ifndef VOLTAGENOTIFICATIONTASK_HH_
#define VOLTAGENOTIFICATIONTASK_HH_

#include <Cosa/Alarm.hh>
#include <Cosa/AnalogPin.hh>

#include "ActivationNetwork.hh"
#include "LedPanel.hh"

class VoltageNotificationTask: public Alarm
{
public:
	VoltageNotificationTask(::Clock* clock, uint32_t period, ActivationTransmitter& transmitter)
		:	Alarm(clock, period),
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
