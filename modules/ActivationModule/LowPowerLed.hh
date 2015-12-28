#ifndef LOWPOWERLED_HH_
#define LOWPOWERLED_HH_

#include <util/delay.h>
#include <Cosa/OutputPin.hh>
#include <Cosa/Periodic.hh>

class LowPowerLed: private Periodic, private OutputPin
{
public:
	LowPowerLed(Board::DigitalPin pin, Job::Scheduler* scheduler, uint8_t period_msecs = REFRESH_MS)
		:Periodic(scheduler, period_msecs), OutputPin(pin, 0) {}

	inline void set(int value)
	{
		if (value) on(); else off();
	}
	inline void toggle()
	{
		set(!Periodic::is_started());
	}
	inline void on()
	{
		Periodic::start();
	}
	inline void off()
	{
		OutputPin::off();
		Periodic::stop();
	}
	
	virtual void run()
	{
		OutputPin::on();
		DELAY(LIT_TIME_US);
		OutputPin::off();
	}
	
private:
	// if REFRESH_MS > 16, then the LED will blink instead of appearing
	// NB: that default value may be too long, depending on MCU activity...
	static const uint8_t REFRESH_MS = 16;
	
	static const uint16_t LIT_TIME_US = 500;
};

#endif /* LOWPOWERLED_HH_ */
