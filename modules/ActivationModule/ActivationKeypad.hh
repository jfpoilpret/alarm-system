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

//TODO Maybe we should externalize all pins selection to the main code?
static const Board::DigitalPin OUTPUT_PINS[] =
{
	Board::D7,
	Board::D2,
	Board::D3,
	Board::D5
};
static const Board::DigitalPin INPUT_PINS[] =
{
	Board::D6,
	Board::D8,
	Board::D4
};
static const int OUTPUTS = sizeof(OUTPUT_PINS) / sizeof(Board::DigitalPin);
static const int INPUTS = sizeof(INPUT_PINS) / sizeof(Board::DigitalPin);
static const char KEYPAD_MAP[INPUTS][OUTPUTS] =
{
	{'1', '4', '7', '*'},
	{'2', '5', '8', '0'},
	{'3', '6', '9', '#'}
};

//TODO Maybe we should externalize all pins selection to the main code?
// Size of secret code to activate/deactivate alarm
static const uint8_t SIZE = 6;

class ActivationKeypad: public BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>
{
public:
	ActivationKeypad()
		:	BufferedMatrixKeypad(INPUT_PINS, OUTPUT_PINS, KEYPAD_MAP, "#*", SHIFT_BUFFER),
		 	locked(Board::D14, 0),
		 	unlocked(Board::D15, 0),
		 	typing(Board::D16, 0) {}

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
