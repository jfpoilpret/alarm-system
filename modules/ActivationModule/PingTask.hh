#ifndef PINGTASK_HH_
#define PINGTASK_HH_

#include <Cosa/Alarm.hh>

#include "ActivationNetwork.hh"
#include "CommonTasks.hh"
#include "LedPanel.hh"

class PingTask: public DefaultPingTask
{
public:
	PingTask(::Clock* clock, uint32_t period, ActivationTransmitter& transmitter, LedPanel& ledPanel)
		:DefaultPingTask(clock, period, transmitter), _ledPanel(ledPanel) {}

	virtual void status_changed(LockStatus status)
	{
		// Dispatch status to LedPanel
		switch (status)
		{
		case UNKNOWN:
			_ledPanel.setLocked(false);
			_ledPanel.setUnlocked(false);
			break;

		case LOCKED:
			_ledPanel.setLocked(true);
			_ledPanel.setUnlocked(false);
			break;

		case UNLOCKED:
			_ledPanel.setLocked(false);
			_ledPanel.setUnlocked(true);
			break;
		}
	}

private:
	LedPanel& _ledPanel;
};

#endif /* PINGTASK_HH_ */
