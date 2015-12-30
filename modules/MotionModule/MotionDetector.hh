#ifndef MOTIONDETECTOR_HH
#define	MOTIONDETECTOR_HH

#include <Cosa/Event.hh>
#include <Cosa/PinChangeInterrupt.hh>
#include "Pins.hh"

class MotionDetector: public PinChangeInterrupt
{
public:
	static const uint8_t MOTION_EVENT = Event::USER_TYPE + 1;
	
	MotionDetector(Event::Handler* handler);
	virtual void on_interrupt(uint16_t arg);
	
private:
	Event::Handler* _handler;
};

#endif	/* MOTIONDETECTOR_HH */

