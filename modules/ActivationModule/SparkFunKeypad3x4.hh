/*
 * SparkFunKeypad3x4.hh
 *
 *  Created on: 18 janv. 2015
 *      Author: Jean-François
 */

#ifndef SPARKFUNKEYPAD3X4_HH_
#define SPARKFUNKEYPAD3X4_HH_

#include <Cosa/Linkage.hh>

#include "MatrixKeypad.hh"

static const int OUTPUTS = 4;
static const int INPUTS = 3;
static const char KEYPAD_MAP[INPUTS][OUTPUTS] =
{
	{'1', '4', '7', '*'},
	{'2', '5', '8', '0'},
	{'3', '6', '9', '#'}
};

template<uint8_t SIZE>
class SparkFunKeypad3x4: public BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>
{
public:
	SparkFunKeypad3x4(	const Board::DigitalPin inputs[INPUTS],
						const Board::DigitalPin outputs[OUTPUTS],
						const uint8_t eventType,
						const char* validate = "#*",
						const BufferInputOverflowBehavior overflowBehavior = SHIFT_BUFFER)
		:	BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>(
				inputs, outputs, KEYPAD_MAP, validate, overflowBehavior),
		 	_eventType(eventType) {}

	struct LockEventParam
	{
		char input[SIZE + 1];
		bool lock;
	};

	void attachListener(::Linkage *listener)
	{
		_listeners.attach(listener);
	}

protected:
	virtual void on_typing(char key) { UNUSED(key); }
	virtual void on_change(char key);
	virtual void on_input(const char* input, char validate);

private:
	Head _listeners;
	const uint8_t _eventType;
};

template<uint8_t SIZE>
void SparkFunKeypad3x4<SIZE>::on_change(char key)
{
	on_typing(key);
	BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>::on_change(key);
}

template<uint8_t SIZE>
void SparkFunKeypad3x4<SIZE>::on_input(const char* input, char validate)
{
	//FIXME Not very good way to pass input...
	static LockEventParam param;

	strcpy(param.input, input);
	param.lock = (validate == '*');
	Event::push(_eventType, &_listeners, &param);
}

#endif /* SPARKFUNKEYPAD3X4_HH_ */
