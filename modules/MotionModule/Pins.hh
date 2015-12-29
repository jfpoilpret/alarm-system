#ifndef PINS_HH_
#define PINS_HH_

#include <Cosa/Board.hh>

//TODO Pins for Motion Detector

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
