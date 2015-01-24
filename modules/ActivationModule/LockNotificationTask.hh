/*
 * LockNotificationTask.hh
 *
 *  Created on: 22 janv. 2015
 *      Author: Jean-François
 */

#ifndef LOCKNOTIFICATIONTASK_HH_
#define LOCKNOTIFICATIONTASK_HH_

#include <Cosa/Linkage.hh>

#include "ActivationNetwork.hh"
#include "MatrixKeypad.hh"

class LockNotificationTask: public Link
{
public:
	LockNotificationTask(ActivationTransmitter& transmitter, LedPanel& ledPanel)
		:	Link(),
		 	_transmitter(transmitter),
		 	_ledPanel(ledPanel) {}

    virtual void on_event(uint8_t type, uint16_t value)
    {
    	if (type == ActivationKeypad::LOCK_EVENT)
    	{
    		// Notify server that a lock/unlock code has been input
    		ActivationKeypad::LockEventParam* param = (ActivationKeypad::LockEventParam*) value;
    		bool status = _transmitter.sendCodeAndGetLockStatus(param->input, param->lock);
    		// Dispatch status to LedPanel
    		_ledPanel.updateStatus(status);
    	}
    }

private:
	ActivationTransmitter& _transmitter;
	LedPanel& _ledPanel;
};

#endif /* LOCKNOTIFICATIONTASK_HH_ */
