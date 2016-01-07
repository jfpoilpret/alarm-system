#ifndef COMMONTASKS_HH_
#define COMMONTASKS_HH_

#include <Cosa/Alarm.hh>
#include <Cosa/AnalogPin.hh>

#include "NetworkUtils.hh"

class AbstractTask: public Alarm
{
public:
	AbstractTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter);

protected:
	AbstractTransmitter& _transmitter;
};

class DefaultPingTask: public AbstractTask
{
public:
	DefaultPingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter);

	virtual void run();
	
protected:
	virtual void status_changed(LockStatus status);
	
private:
	LockStatus _status;
};

class VoltageNotificationTask: public AbstractTask
{
public:
	VoltageNotificationTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter);
	virtual void run();
};

#endif /* COMMONTASKS_HH_ */
