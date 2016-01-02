#ifndef LOCKNOTIFICATIONTASK_HH_
#define LOCKNOTIFICATIONTASK_HH_

#include <Cosa/Event.hh>

#include "ActivationNetwork.hh"
#include "MatrixKeypad.hh"

class LockNotificationTask: public Event::Handler
{
public:
	LockNotificationTask(ActivationTransmitter& transmitter, LedPanel& ledPanel)
		:	Handler(),
		 	_transmitter(transmitter),
		 	_ledPanel(ledPanel) {}

	virtual void on_event(uint8_t type, uint16_t value)
	{
		if (type == ActivationKeypad::LOCK_EVENT)
		{
			// Notify server that a lock/unlock code has been input
			ActivationKeypad* keypad = (ActivationKeypad*) value;
			char input[ActivationKeypad::INPUT_SIZE + 1];
			keypad->input(input);
			bool lock = (keypad->validate() == '*');
			keypad->clear();
			LockStatus status = _transmitter.sendCodeAndGetLockStatus(input, lock);
			// Dispatch status to LedPanel
			//TODO refactor this code (same in PingTask.hh)
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
	}

private:
	ActivationTransmitter& _transmitter;
	LedPanel& _ledPanel;
};

#endif /* LOCKNOTIFICATIONTASK_HH_ */
