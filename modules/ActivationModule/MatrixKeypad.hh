/*
 * MatrixKeypad.hh
 */

#ifndef MATRIXKEYPAD_HH_
#define MATRIXKEYPAD_HH_

#include <Cosa/Linkage.hh>
#include <Cosa/InputPin.hh>
#include <Cosa/OutputPin.hh>
#include <Cosa/Watchdog.hh>

#include "ArrayAlloc.hh"

class InputsInit
{
public:
	InputsInit(const Board::DigitalPin* pins):_pins(pins) {}
	const InputPin operator()(int i) const { return InputPin(_pins[i], InputPin::Mode::PULLUP_MODE); }
private:
	const Board::DigitalPin* _pins;
};

class OutputsInit
{
public:
	OutputsInit(const Board::DigitalPin* pins):_pins(pins) {}
	const OutputPin operator()(int i) const { return OutputPin(_pins[i], 1); }
private:
	const Board::DigitalPin* _pins;
};

template<int INPUTS, int OUTPUTS>
class MatrixKeypad: private Link
{
public:
	MatrixKeypad(	const Board::DigitalPin inputs[INPUTS],
					const Board::DigitalPin outputs[OUTPUTS],
					const char mapping[INPUTS][OUTPUTS])
		:	_inputs(InputsInit(inputs)),
		 	_outputs(OutputsInit(outputs)),
		 	_mapping((const char*) mapping),
		 	_key(0) {}

	void begin()
		__attribute__((always_inline))
	{
		Watchdog::attach(this, SAMPLE_MS);
	}

	void end()
		__attribute__((always_inline))
	{
		detach();
	}

private:
	virtual void on_change(char key) = 0;

	virtual void on_event(uint8_t type, uint16_t value)
	{
		UNUSED(value);
		// Skip all but timeout events
		if (type != Event::TIMEOUT_TYPE) return;

		// Update the button state
		char old_key = _key;
		_key = scan();
		char new_key = _key;

		// If changed according to mode call the pin change handler
		if (old_key != new_key)
			on_change(new_key);
	}

	char scan()
	{
		char result = 0;
		for (int i = 0; i < OUTPUTS; i++)
		{
			_outputs[i].off();
			for (int j = 0; j < INPUTS; j++)
			{
				if (_inputs[j].is_off())
				{
					result = _mapping[j * OUTPUTS + i];
					break;
				}
			}
			_outputs[i].on();
			if (result)
				break;
		}
		return result;
	}

	/** Keypad sampling period in milli-seconds. */
	static const uint16_t SAMPLE_MS = 64;

	// static storage for rows and columns pins instances
	ArrayAlloc<INPUTS, InputPin> _inputs;
	ArrayAlloc<OUTPUTS, OutputPin> _outputs;
	// character mapping
	const char* _mapping;
	char _key;
};

template<int INPUTS, int OUTPUTS, int BUFSIZE>
class BufferedMatrixKeypad: public MatrixKeypad<INPUTS, OUTPUTS>
{
public:
	enum OverflowBehavior
	{
		REJECT_KEY,
		SHIFT_BUFFER,
		RESET_BUFFER
	}
	__attribute__((packed));

	BufferedMatrixKeypad(	const Board::DigitalPin inputs[INPUTS],
							const Board::DigitalPin outputs[OUTPUTS],
							const char mapping[INPUTS][OUTPUTS],
							const char validate,
							const char cancel = 0,
							const OverflowBehavior overflowBehavior = REJECT_KEY)
		:	MatrixKeypad<INPUTS, OUTPUTS>(inputs, outputs, mapping),
			_validate(validate),
			_cancel(cancel),
			_overflowBehavior(overflowBehavior)
	{
		clear();
	}

	void clear() {
		_index = 0;
		memset(_input, 0, BUFSIZE + 1);
	}

	char* input(char* buffer) const
	{
		strcpy(buffer, _input);
		return buffer;
	}

private:
	virtual void on_input(const char* input) = 0;
	virtual void on_cancel(const char* input)
	{
		UNUSED(input);
	}
	virtual void on_overflow(const char* input, char key)
	{
		UNUSED(input);
		UNUSED(key);
	}

	void on_change(char key)
	{
		if (!key) return;
		if (key == _cancel)
		{
			on_cancel(_input);
			clear();
		}
		else if (key == _validate)
		{
			on_input(_input);
			clear();
		}
		else if (_index < BUFSIZE)
			_input[_index++] = key;
		else
		{
			on_overflow(_input, key);
			switch (_overflowBehavior)
			{
			case RESET_BUFFER:
				clear();
				_input[_index++] = key;
				break;

			case SHIFT_BUFFER:
				strcpy(_input, _input + 1);
				//FIXME Check that the replacement line is now OK
//				_input[--_index] = key;
				_input[_index - 1] = key;
				break;

			case REJECT_KEY:
			default:
				// Do nothing
				break;
			}
		}
	}

	const char _validate;
	const char _cancel;
	const OverflowBehavior _overflowBehavior;
	uint8_t _index;
	char _input[BUFSIZE + 1];
};


#endif /* MATRIXKEYPAD_HH_ */
