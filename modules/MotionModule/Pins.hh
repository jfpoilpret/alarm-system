#ifndef PINS_HH_
#define PINS_HH_

#include <Cosa/Board.hh>

// Pin used to communicate to DS18B20
static const Board::DigitalPin TEMP_SENSOR_PIN	= Board::D0;

// Pin used for PIR output connection (interrupt)
#ifdef BOARD_ATTINYX4
static const Board::InterruptPin PIR_OUTPUT = Board::PCI7;
#else
static const Board::InterruptPin PIR_OUTPUT = Board::PCI3;
#endif

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
