#ifndef PINS_HH_
#define PINS_HH_

#include <Cosa/Board.hh>

// Pins used for device address configuration (2-bits only)
static const Board::DigitalPin CONFIG_ID1	= Board::D0;
static const Board::DigitalPin CONFIG_ID2	= Board::D1;

// Pin used for PIR output connection (interrupt)
static const Board::InterruptPin PIR_OUTPUT = Board::PCI3;

// Pins used to connect to NRF24L01 (in addition to SPI pins: SCK, MISO, MOSI)
//
// NRF24L01 wiring
//                          NRF24L01P
//                       +------------+
// (GND)---------------1-|GND         |
// (3V3)---------------2-|VCC         |
// (D8)----------------3-|CE          |
// (D9)----------------4-|CSN         |
// (D4/SCK)------------5-|SCK         |
// (D5/MOSI)-----------6-|MOSI        |
// (D6/MISO)-----------7-|MISO        |
// (D10/EXT0)----------8-|IRQ         |
//                       +------------+
//
static const Board::DigitalPin RF_CE = Board::D8;
static const Board::DigitalPin RF_CSN = Board::D9;
static const Board::ExternalInterruptPin RF_IRQ = Board::EXT0;

#endif /* PINS_HH_ */
