#ifndef PINGTASK_HH
#define	PINGTASK_HH

#include "CommonTasks.hh"

class PingTask: public DefaultPingTask
{
public:
	PingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter);
		
protected:
	virtual void status_changed(LockStatus status);
};


#endif	/* PINGTASK_HH */

