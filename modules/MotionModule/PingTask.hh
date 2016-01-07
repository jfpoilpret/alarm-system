#ifndef PINGTASK_HH
#define	PINGTASK_HH

#include <Cosa/PinChangeInterrupt.hh>
#include "CommonTasks.hh"
#include "MotionDetector.hh"

class PingTask: public DefaultPingTask
{
public:
	PingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter, MotionDetector& detector);
//	PingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter, PinChangeInterrupt& detector);
		
protected:
	virtual void status(LockStatus status);

private:
	MotionDetector& _detector;	
//	PinChangeInterrupt& _detector;	
};


#endif	/* PINGTASK_HH */

