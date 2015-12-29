#ifndef COMMONTASKS_HH_
#define COMMONTASKS_HH_

#include <Cosa/Alarm.hh>
#include <Cosa/AnalogPin.hh>

#include "NetworkUtils.hh"

class AbstractTask: public Alarm
{
public:
	AbstractTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter)
		:	Alarm(clock, period),
		 	_transmitter(transmitter) {}

protected:
	AbstractTransmitter& _transmitter;
};


class DefaultPingTask: public AbstractTask
{
public:
	DefaultPingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter)
		:AbstractTask(clock, period, transmitter) {}

	virtual void run()
	{
		// Get lock status from server
		status(_transmitter.pingServerAndGetLockStatus());
	}
	
	virtual void status(LockStatus status)
	{
		UNUSED(status);
	}
};

class VoltageNotificationTask: public AbstractTask
{
public:
	VoltageNotificationTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter)
		:AbstractTask(clock, period, transmitter) {}

	virtual void run()
	{
		// Get current voltage level
		uint16_t bandgap = AnalogPin::bandgap();

		// Send it to server
		_transmitter.sendVoltageLevel(bandgap);
	}
};

#endif /* COMMONTASKS_HH_ */
