#include <Cosa/Board.hh>
#include <Cosa/OutputPin.hh>
#include <Cosa/Watchdog.hh>

#include "ActivationKeypad.hh"

static ActivationKeypad keypad;

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
