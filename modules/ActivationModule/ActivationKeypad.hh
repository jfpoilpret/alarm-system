/*
 * ActivationKeypad.hh
 *
 *  Created on: 18 janv. 2015
 *      Author: Jean-François
 */

#ifndef ACTIVATIONKEYPAD_HH_
#define ACTIVATIONKEYPAD_HH_

#include <Cosa/Linkage.hh>

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

//TODO Create a generic Keypad4x3<SIZE>(inputs, outputs, eventype, const char* =, Overflow=) class
// Then create a subclass for Activation
class ActivationKeypad: public BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>
{
public:
	ActivationKeypad()
		:	BufferedMatrixKeypad(INPUT_PINS, OUTPUT_PINS, KEYPAD_MAP, "#*", SHIFT_BUFFER),
		 	_typing(LED_TYPING, 0) {}

	//TODO make it a parameter of the constructor?
	static const uint8_t LOCK_EVENT = Event::USER_TYPE + 1;

	struct LockEventParam
	{
		char input[SIZE + 1];
		bool lock;
	};

	void attachLockListener(::Linkage *listener)
	{
		_listeners.attach(listener);
	}

protected:
	virtual void on_change(char key);
	virtual void on_input(const char* input, char validate);

private:
	OutputPin _typing;
	Head _listeners;
};

void ActivationKeypad::on_change(char key)
{
	_typing.set(key);
	BufferedMatrixKeypad::on_change(key);
}

void ActivationKeypad::on_input(const char* input, char validate)
{
	//TODO Not very good way to pass input...
	static LockEventParam param;

	strcpy(param.input, input);
	param.lock = (validate == '*');
	Event::push(LOCK_EVENT, &_listeners, &param);
}

#endif /* ACTIVATIONKEYPAD_HH_ */
