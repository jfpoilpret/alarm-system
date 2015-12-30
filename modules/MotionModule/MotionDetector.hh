#ifndef MOTIONDETECTOR_HH
#define	MOTIONDETECTOR_HH

#include <Cosa/Event.hh>
#include <Cosa/PinChangeInterrupt.hh>
#include "Pins.hh"

class MotionDetector: public PinChangeInterrupt
{
public:
	static const uint8_t MOTION_EVENT = Event::USER_TYPE + 1;
	
	MotionDetector():PinChangeInterrupt(PIR_OUTPUT, PinChangeInterrupt::ON_RISING_MODE) {}
	virtual void on_interrupt(uint16_t arg);
	inline void attachHandler(Event::Handler *handler)
	{
		_handler = handler;
	}
	
private:
	Event::Handler* _handler;
};

#endif	/* MOTIONDETECTOR_HH */

