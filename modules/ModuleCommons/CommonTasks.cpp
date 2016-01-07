#include "CommonTasks.hh"

AbstractTask::AbstractTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter)
: Alarm(clock, period), _transmitter(transmitter) {}

DefaultPingTask::DefaultPingTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter)
: AbstractTask(clock, period, transmitter), _status(UNKNOWN) {}

void DefaultPingTask::run()
{
	// Get lock status from server
	LockStatus new_status = _transmitter.pingServerAndGetLockStatus();
	if (new_status != _status)
	{
		_status = new_status;
		status_changed(_status);
	}
}

void DefaultPingTask::status_changed(LockStatus status)
{
	UNUSED(status);
}

VoltageNotificationTask::VoltageNotificationTask(::Clock* clock, uint32_t period, AbstractTransmitter& transmitter)
: AbstractTask(clock, period, transmitter) {}

void VoltageNotificationTask::run()
{
	// Get current voltage level
	uint16_t bandgap = AnalogPin::bandgap();

	// Send it to server
	_transmitter.sendVoltageLevel(bandgap);
}
