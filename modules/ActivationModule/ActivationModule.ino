#include <Cosa/Board.hh>
#include <Cosa/OutputPin.hh>
#include <Cosa/Watchdog.hh>

#include "MatrixKeypad.hh"

static const Board::DigitalPin OUTPUT_PINS[] = {Board::D7,Board::D2,Board::D3,Board::D5};
static const Board::DigitalPin INPUT_PINS[] = {Board::D6,Board::D8,Board::D4};
static const int OUTPUTS = sizeof(OUTPUT_PINS) / sizeof(Board::DigitalPin);
static const int INPUTS = sizeof(INPUT_PINS) / sizeof(Board::DigitalPin);
static const char KEYPAD_MAP[INPUTS][OUTPUTS] = {{'1', '4', '7', '*'}, {'2', '5', '8', '0'}, {'3', '6', '9', '#'}};

const uint8_t SIZE = 6;

//TODO LED that blinks during typing
class Keypad4x3: public BufferedMatrixKeypad<INPUTS, OUTPUTS, SIZE>
{
public:
	Keypad4x3()
		:	BufferedMatrixKeypad(INPUT_PINS, OUTPUT_PINS, KEYPAD_MAP, '#', '*', SHIFT_BUFFER),
		 	ok(Board::LED, 0) {}
//			typing(Board::A0), ok(Board::LED) {}

private:
//	virtual void on_change(char key)
//	{
//		typing.set(key);
//		BufferedMatrixKeypad::on_change(key);
//	}

	virtual void on_input(const char* input)
	{
		ok.set(strcmp(input, "123456") == 0);
	}

//	OutputPin typing;
	OutputPin ok;
};

static Keypad4x3 keypad;

//The setup function is called once at startup of the sketch
void setup()
{
	// Initialize power settings
	Power::twi_disable();
	Power::adc_disable();
	Power::timer0_disable();
	Power::timer1_disable();
	Power::timer2_disable();
	// SPI shall be enabled when adding RF
	Power::spi_disable();
	// USART shall be disabled on final module
	Power::usart0_disable();

	// Sleep modes by order or increasing consumption
	// Lowest consumption mode (works on Arduino, not tested yet on breadboard ATmega)
	Power::set(SLEEP_MODE_PWR_DOWN);		// 0.36mA

//	Power::set(SLEEP_MODE_STANDBY);			// 0.84mA
//	Power::set(SLEEP_MODE_PWR_SAVE);		// 1.65mA
//	Power::set(SLEEP_MODE_EXT_STANDBY);		// 1.65mA
//	Power::set(SLEEP_MODE_ADC);				// 6.5 mA

	// Only this mode works when using serial output
//	Power::set(SLEEP_MODE_IDLE);			// 15mA

	Watchdog::begin(64, Watchdog::push_timeout_events);
	keypad.begin();
}

// The loop function is called in an endless loop
void loop()
{
	Watchdog::await();
	Event event;
	while (Event::queue.dequeue(&event))
		event.dispatch();
}
