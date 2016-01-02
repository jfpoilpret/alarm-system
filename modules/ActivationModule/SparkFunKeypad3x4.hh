#ifndef SPARKFUNKEYPAD3X4_HH_
#define SPARKFUNKEYPAD3X4_HH_

#include <Cosa/Event.hh>

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
	SparkFunKeypad3x4(	Job::Scheduler* scheduler,
						const Board::DigitalPin inputs[INPUTS],
						const Board::DigitalPin outputs[OUTPUTS],
						const uint8_t eventType,
						Event::Handler* handler,
						const char* validate = "#*",
						const BufferInputOverflowBehavior overflowBehavior = SHIFT_BUFFER)
		:	BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>(
				scheduler, inputs, outputs, KEYPAD_MAP, validate, overflowBehavior),
		 	_eventType(eventType), _handler(handler), _validate(0) {}

	char validate() const
	{
		return _validate;
	}

	static const uint8_t INPUT_SIZE = SIZE;

protected:
	virtual void on_input(const char* input, char validate);

private:
	const uint8_t _eventType;
	Event::Handler* _handler;
	char _validate;
};

template<uint8_t SIZE>
void SparkFunKeypad3x4<SIZE>::on_input(const char* input, char validate)
{
	UNUSED(input);
	_validate = validate;
	Event::push(_eventType, _handler, this);
}

#endif /* SPARKFUNKEYPAD3X4_HH_ */
