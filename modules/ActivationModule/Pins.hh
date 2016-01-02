#ifndef PINS_HH_
#define PINS_HH_

#include <Cosa/Board.hh>

// Pins used to connect to the 4x3 Keypad (sparkfun COM-086553)
//
// KEYPAD wiring
//                         KEYPAD 4x3
//                       +------------+
// (D8)----------------1-|COL2        |
// (D7)----------------2-|ROW1        |
// (D6)----------------3-|COL1        |
// (D5)----------------4-|ROW4        |
// (D3)----------------5-|COL3        |
// (D4)----------------6-|ROW3        |
// (D1)----------------7-|ROW2        |
//                       +------------+
//
// Pins used to connect to keyboard columns (outputs)
static const Board::DigitalPin KEYPAD_ROW_1 = Board::D7;
static const Board::DigitalPin KEYPAD_ROW_2 = Board::D1;
static const Board::DigitalPin KEYPAD_ROW_3 = Board::D4;
static const Board::DigitalPin KEYPAD_ROW_4 = Board::D5;

// Pins used to connect to keyboard rows (inputs)
static const Board::DigitalPin KEYPAD_COL_1 = Board::D6;
static const Board::DigitalPin KEYPAD_COL_2 = Board::D8;
static const Board::DigitalPin KEYPAD_COL_3 = Board::D3;

// Pins used to connect to feedback LEDs anode
static const Board::DigitalPin LED_LOCKED	= Board::D15;		// A1 on UNO (Red)
static const Board::DigitalPin LED_UNLOCKED	= Board::D14;		// A0 on UNO (Green)
static const Board::DigitalPin LED_TYPING	= Board::D16;		// A2 on UNO (Yellow)

// Pin available for debugging
static const Board::DigitalPin LED_DEBUG	= Board::D17;		// A3 on UNO (Red or Yellow)

// Pins used for device address configuration (2-bits only)
static const Board::DigitalPin CONFIG_ID1	= Board::D18;		// A4 on UNO
static const Board::DigitalPin CONFIG_ID2	= Board::D19;		// A5 on UNO


// Pins used to connect to NRF24L01 (in addition to SPI pins: SCK, MISO, MOSI)
//
// NRF24L01 wiring
//                          NRF24L01P
//                       +------------+
// (GND)---------------1-|GND         |
// (3V3)---------------2-|VCC         |
// (D9)----------------3-|CE          |
// (D10)---------------4-|CSN         |
// (D13/SCK)-----------5-|SCK         |
// (D11/MOSI)----------6-|MOSI        |
// (D12/MISO)----------7-|MISO        |
// (D2/EXT0)-----------8-|IRQ         |
//                       +------------+
//
static const Board::DigitalPin RF_CE = Board::D9;
static const Board::DigitalPin RF_CSN = Board::D10;
static const Board::ExternalInterruptPin RF_IRQ = Board::EXT0;

#endif /* PINS_HH_ */
