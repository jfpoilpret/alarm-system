/*
 * ActivationKeypad.hh
 *
 *  Created on: 18 janv. 2015
 *      Author: Jean-François
 */

#ifndef ACTIVATIONKEYPAD_HH_
#define ACTIVATIONKEYPAD_HH_

#include "LowPowerLed.hh"
#include "SparkFunKeypad3x4.hh"

#include "Pins.hh"

static const Board::DigitalPin OUTPUT_PINS[] =
{
	KEYPAD_ROW_1,
	KEYPAD_ROW_2,
	KEYPAD_ROW_3,
	KEYPAD_ROW_4
};
static const Board::DigitalPin INPUT_PINS[] =
{
	KEYPAD_COL_1,
	KEYPAD_COL_2,
	KEYPAD_COL_3
};

//TODO Maybe we should externalize SIZE to the main code?
// Size of secret code to activate/deactivate alarm
static const uint8_t SIZE = 6;

class ActivationKeypad: public SparkFunKeypad3x4<SIZE>
{
public:
	ActivationKeypad()
		:	SparkFunKeypad3x4<SIZE>(INPUT_PINS, OUTPUT_PINS, LOCK_EVENT),
		 	_typing(LED_TYPING, 0) {}

	static const uint8_t LOCK_EVENT = Event::USER_TYPE + 1;

protected:
	virtual void on_typing(char key)
	{
		_typing.set(key);
	}

private:
	OutputPin _typing;
};

#endif /* ACTIVATIONKEYPAD_HH_ */
