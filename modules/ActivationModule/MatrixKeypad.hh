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

protected:
	virtual void on_change(char key) = 0;

private:
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

	virtual void on_event(uint8_t type, uint16_t value);

	char scan();

	/** Keypad sampling period in milli-seconds. */
	static const uint16_t SAMPLE_MS = 64;

	// static storage for rows and columns pins instances
	ArrayAlloc<INPUTS, InputPin> _inputs;
	ArrayAlloc<OUTPUTS, OutputPin> _outputs;
	// character mapping
	const char* _mapping;
	char _key;
};

enum BufferInputOverflowBehavior
{
	REJECT_KEY,
	SHIFT_BUFFER,
	RESET_BUFFER
}
__attribute__((packed));

template<int INPUTS, int OUTPUTS, int BUFSIZE>
class BufferedMatrixKeypad: public MatrixKeypad<INPUTS, OUTPUTS>
{
public:
	BufferedMatrixKeypad(	const Board::DigitalPin inputs[INPUTS],
							const Board::DigitalPin outputs[OUTPUTS],
							const char mapping[INPUTS][OUTPUTS],
							const char* validate,
							const BufferInputOverflowBehavior overflowBehavior = REJECT_KEY)
		:	MatrixKeypad<INPUTS, OUTPUTS>(inputs, outputs, mapping),
			_validate(validate),
			_overflowBehavior(overflowBehavior)
	{
		clear();
	}

	void clear() {
		_index = 0;
		memset(_input, 0, BUFSIZE + 1);
	}

	char* input(char* buffer) const
		__attribute__((always_inline))
	{
		return strcpy(buffer, _input);
	}

protected:
	virtual void on_input(const char* input, char validate) = 0;
	virtual void on_overflow(const char* input, char key)
	{
		UNUSED(input);
		UNUSED(key);
	}
	void on_change(char key);

private:
	const char* _validate;
	const BufferInputOverflowBehavior _overflowBehavior;
	uint8_t _index;
	char _input[BUFSIZE + 1];
};

template<int INPUTS, int OUTPUTS>
void MatrixKeypad<INPUTS, OUTPUTS>::on_event(uint8_t type, uint16_t value)
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

template<int INPUTS, int OUTPUTS>
char MatrixKeypad<INPUTS, OUTPUTS>::scan()
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

template<int INPUTS, int OUTPUTS, int BUFSIZE>
void BufferedMatrixKeypad<INPUTS, OUTPUTS, BUFSIZE>::on_change(char key)
{
	if (!key) return;
	if (strchr(_validate, key) != 0)
	{
		on_input(_input, key);
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
			_input[_index - 1] = key;
			break;

		case REJECT_KEY:
		default:
			// Do nothing
			break;
		}
	}
}

#endif /* MATRIXKEYPAD_HH_ */
