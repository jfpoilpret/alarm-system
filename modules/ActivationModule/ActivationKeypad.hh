/*
 * ActivationKeypad.hh
 *
 *  Created on: 18 janv. 2015
 *      Author: Jean-François
 */

#ifndef ACTIVATIONKEYPAD_HH_
#define ACTIVATIONKEYPAD_HH_

#include "LowPowerLed.hh"
#include "MatrixKeypad.hh"

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
static const int OUTPUTS = sizeof(OUTPUT_PINS) / sizeof(Board::DigitalPin);
static const int INPUTS = sizeof(INPUT_PINS) / sizeof(Board::DigitalPin);
static const char KEYPAD_MAP[INPUTS][OUTPUTS] =
{
	{'1', '4', '7', '*'},
	{'2', '5', '8', '0'},
	{'3', '6', '9', '#'}
};

//TODO Maybe we should externalize SIZE to the main code?
// Size of secret code to activate/deactivate alarm
static const uint8_t SIZE = 6;

class ActivationKeypad: public BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>
{
public:
	ActivationKeypad()
		:	BufferedMatrixKeypad(INPUT_PINS, OUTPUT_PINS, KEYPAD_MAP, "#*", SHIFT_BUFFER),
		 	locked(LED_LOCKED, 0),
		 	unlocked(LED_UNLOCKED, 0),
		 	typing(LED_TYPING, 0) {}

protected:
	virtual void on_change(char key);
	virtual void on_input(const char* input, char validate);

private:
	LowPowerLed locked;
	LowPowerLed unlocked;
	OutputPin typing;
};

void ActivationKeypad::on_change(char key)
{
	typing.set(key);
	BufferedMatrixKeypad::on_change(key);
}

void ActivationKeypad::on_input(const char* input, char validate)
{
	//TODO this is for tests only
	//TODO instead we should encrypt the input, send it to the center, wait for ack and update the LEDs
	//TODO Maybe we should just trigger a user event here instead?
	//TODO Maybe unlocked/locked LEDs should be handled somewhere else?
	if (strcmp(input, "123456") == 0)
	{
		bool unlock = (validate == '#');
		bool lock = (validate == '*');
		unlocked.set(unlock);
		locked.set(lock);
	}
}

#endif /* ACTIVATIONKEYPAD_HH_ */
