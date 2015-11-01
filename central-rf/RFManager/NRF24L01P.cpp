/**
 * @file NRF24L01P.cpp
 * @version 1.0
 *
 * @section License
 * Copyright (C) 2013-2015, Jean-François Poilprêt
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * This file is inspired from NRF 24L01 library of the Arduino Che Cosa project.
 * It allows Raspberry Pi programs to "talk" to Arduino using Cosa with NRF24L01 
 * device.
 */

#include "NRF24L01P.h"

#include <iostream>
#include <time.h>

static timespec current_time() {
	timespec time;
	clock_gettime(CLOCK_REALTIME, &time);
	return time;
}

static uint32_t ms_since(const timespec& since) {
	timespec now = current_time();
	return (now.tv_sec - since.tv_sec) * 1000 + (now.tv_nsec - since.tv_nsec) / 1000000;
}

static uint64_t us_since(const timespec& since) {
	timespec now = current_time();
	return (now.tv_sec - since.tv_sec) * 1000000 + (now.tv_nsec - since.tv_nsec) / 1000;
}

NRF24L01P::NRF24L01P(uint16_t net, uint8_t dev, RPiGPIOPin csn, RPiGPIOPin ce, RPiGPIOPin irq)
	:	m_addr(net, dev),
		m_csn(csn),
		m_ce(ce),
		m_irq(irq),
		m_channel(DEFAULT_CHANNEL),
		m_status(0),
		m_state(POWER_DOWN_STATE),
		m_dest(0),
		m_trans(0),
		m_retrans(0),
		m_drops(0),
		m_missing_irq(0) {
	// Setup BCM2835 and SPI
	bcm2835_init();
	bcm2835_spi_begin();
	bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
	bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32);
	bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
	bcm2835_spi_chipSelect(BCM2835_SPI_CS_NONE);
	bcm2835_gpio_fsel(m_csn, BCM2835_GPIO_FSEL_OUTP);
	// Setup RX/TX active pin (ce)
	bcm2835_gpio_fsel(m_ce, BCM2835_GPIO_FSEL_OUTP);
	// Setup IRQ pin
	bcm2835_gpio_fsel(m_irq, BCM2835_GPIO_FSEL_INPT);
}

NRF24L01P::~NRF24L01P() {
	std::cout << "NRF24L01P::~NRF24L01P()" << std::endl;
	powerdown();
	bcm2835_spi_end();
	bcm2835_close();
}

void NRF24L01P::begin() {
	// Setup hardware features, channel, bitrate, retransmission, dynamic payload
	write(FEATURE, (_BV(EN_DPL) | _BV(EN_ACK_PAY) | _BV(EN_DYN_ACK)));
	write(RF_CH, m_channel);
	write(RF_SETUP, (RF_DR_2MBPS | RF_PWR_0DBM));
	write(SETUP_RETR, ((DEFAULT_ARD << ARD) | (DEFAULT_ARC << ARC)));
	write(DYNPD, DPL_PA);

	// Setup hardware receive pipes address; network (16-bit), device (8-bit)
	// P0: auto-acknowledge (see set_transmit_mode)
	// P1: node address<network:device> with auto-acknowledge
	// P2: broadcast<network:0>
	addr_t rx_addr = m_addr;
	write(SETUP_AW, AW_3BYTES);
	write(RX_ADDR_P1, &rx_addr, sizeof (rx_addr));
	write(RX_ADDR_P2, BROADCAST);
	write(EN_RXADDR, (_BV(ERX_P2) | _BV(ERX_P1)));
	write(EN_AA, (_BV(ENAA_P1) | _BV(ENAA_P0)));

	// Ready to go
	powerup();
}

uint8_t NRF24L01P::read(Command cmd) {
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(cmd);
	uint8_t res = bcm2835_spi_transfer(NOP);
	bcm2835_gpio_set(m_csn);
	return res;
}

void NRF24L01P::read(Command cmd, void* buf, size_t size) {
	uint8_t* p = (uint8_t*) buf;
	for (size_t i = 0; i < size; i++) *p++ = NOP;
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(cmd);
	bcm2835_spi_transfern((char*) buf, size);
	bcm2835_gpio_set(m_csn);
}

void NRF24L01P::write(Command cmd) {
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(cmd);
	bcm2835_gpio_set(m_csn);
}

void NRF24L01P::write(Command cmd, uint8_t data) {
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(cmd);
	bcm2835_spi_transfer(data);
	bcm2835_gpio_set(m_csn);
}

void NRF24L01P::write(Command cmd, const void* buf, size_t size) {
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(cmd);
	bcm2835_spi_writenb((char*) buf, size);
	bcm2835_gpio_set(m_csn);
}

NRF24L01P::status_t NRF24L01P::read_status() {
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(NOP);
	bcm2835_gpio_set(m_csn);
	return m_status;
}

void NRF24L01P::powerup() {
	if (m_state != POWER_DOWN_STATE) return;
	bcm2835_gpio_clr(m_ce);

	// Setup configuration for powerup and clear interrupts
	write(CONFIG, (_BV(EN_CRC) | _BV(CRCO) | _BV(PWR_UP)));
	delay(Tpd2stby_ms);
	m_state = STANDBY_STATE;

	// Flush status
	write(STATUS, (_BV(RX_DR) | _BV(TX_DS) | _BV(MAX_RT)));
	write(FLUSH_TX);
	write(FLUSH_RX);
}

void NRF24L01P::standby() {
	if (m_state == STANDBY_STATE) return;
	bcm2835_gpio_clr(m_ce);
	m_state = STANDBY_STATE;
}

void NRF24L01P::powerdown() {
	if (m_state == POWER_DOWN_STATE) return;
	bcm2835_gpio_clr(m_ce);
	write(CONFIG, (_BV(EN_CRC) | _BV(CRCO)));
	m_state = POWER_DOWN_STATE;
}

bool NRF24L01P::wait_for_irq(uint32_t max_ms, bool update_missing_irq) {
	timespec start = current_time();
	while (true) {
		if (bcm2835_gpio_lev(m_irq) == LOW) break;
		if ((max_ms != 0) && (ms_since(start) > max_ms)) {
			if (update_missing_irq) m_missing_irq++;
			return false;
		}
		delay(1);
	}
	return true;
}

int NRF24L01P::send(uint8_t dest, uint8_t port, const void* buf, size_t len, uint32_t ms) {
	if (buf == 0) return -EINVAL;
	if (len > PAYLOAD_MAX) return -EMSGSIZE;

	// Setting transmit destination first (needs to ensure standby mode)
	standby();
	// Trigger the transmitter mode
	write(CONFIG, (_BV(EN_CRC) | _BV(CRCO) | _BV(PWR_UP)));
	// Setup primary transmit address
	addr_t tx_addr(m_addr.network, dest);
	write(TX_ADDR, &tx_addr, sizeof (tx_addr));
	// Write source address and payload to the transmit fifo
	uint8_t command = ((dest != BROADCAST) ? W_TX_PAYLOAD : W_TX_PAYLOAD_NO_ACK);
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(command);
	bcm2835_spi_transfer(m_addr.device);
	bcm2835_spi_transfer(port);
	bcm2835_spi_writenb((char*) buf, len);
	bcm2835_gpio_set(m_csn);
	// Check for auto-acknowledge pipe(0), and address setup and enable
	if (dest != BROADCAST) {
		write(RX_ADDR_P0, &tx_addr, sizeof (tx_addr));
		write(EN_RXADDR, _BV(ERX_P2) | _BV(ERX_P1) | _BV(ERX_P0));
	}
	
	m_trans += 1;

	// Pulse CE for 10us in order to start transmission
	bcm2835_gpio_set(m_ce);
	delayMicroseconds(Thce_us);
	bcm2835_gpio_clr(m_ce);
	
	// Wait for transmission
	wait_for_irq(ms, true);

	// Clear IRQ
	status_t status = read_status();
//	bcm2835_gpio_clr(m_ce);
	write(STATUS, (_BV(RX_DR) | _BV(TX_DS) | _BV(MAX_RT)));
	
	// Check for auto-acknowledge pipe(0) disable
	if (dest != BROADCAST) {
		write(EN_RXADDR, (_BV(ERX_P2) | _BV(ERX_P1)));
	}

	bool data_sent = status.tx_ds;

	// Read retransmission counter and update
	observe_tx_t observe = read_observe_tx();
	m_retrans += observe.arc_cnt;

	// Check that the message was delivered
	if (data_sent) return len;

	// Failed to delivery
	write(FLUSH_TX);
	m_drops += 1;

	return -EIO;
}

int NRF24L01P::recv(uint8_t& src, uint8_t& port, void* buf, size_t size, uint32_t ms) {
	// First check if there is some payload in RX FIFO
	if (!read_fifo_status().rx_empty) {
		return read_fifo_payload(src, port, buf, size);
	}
	
	// Run in receiver mode
	if (m_state != RX_STATE) {
		standby();
		// Configure primary receiver mode
		write(CONFIG, (_BV(EN_CRC) | _BV(CRCO) | _BV(PWR_UP) | _BV(PRIM_RX)));
		bcm2835_gpio_set(m_ce);
		delayMicroseconds(Tstby2a_us);
		m_state = RX_STATE;
	}

	// Check if there is data available on any pipe
	if (!wait_for_irq(ms, false)) return -ETIME;
	status_t status =  read_status();
	
	// Go to standby mode and clear IRQ
	standby();
	write(STATUS, (_BV(RX_DR) | _BV(TX_DS) | _BV(MAX_RT)));

	// Check expected status (RX_DR)
	if (!status.rx_dr) return -EIO;

	// Check the receiver fifo
	if (read_fifo_status().rx_empty) {
		// UNEXPECTED BRANCH!
		std::cerr << "RX FIFO EMPTY!!!" << std::endl;
	}

	// Check for payload error from device (Tab. 20, pp. 51, R_RX_PL_WID)
	return read_fifo_payload(src, port, buf, size);
}

int NRF24L01P::read_fifo_payload(uint8_t& src, uint8_t& port, void* buf, size_t size) {
	// Check for payload error from device (Tab. 20, pp. 51, R_RX_PL_WID)
	uint8_t count = read(R_RX_PL_WID) - 2;
	if ((count > PAYLOAD_MAX) || (count > size)) {
		write(FLUSH_RX);
		return -EMSGSIZE;
	}
	
	// Data is available, check if this a broadcast or not
	m_dest = (read_status().rx_p_no == 1 ? m_addr.device : BROADCAST);
	
	// Read the source address, port and payload
	uint8_t* p = (uint8_t*) buf;
	for (size_t i = 0; i < size; i++) *p++ = NOP;
	bcm2835_gpio_clr(m_csn);
	m_status = bcm2835_spi_transfer(R_RX_PAYLOAD);
	src = bcm2835_spi_transfer(0);
	port = bcm2835_spi_transfer(0);
	bcm2835_spi_transfern((char*) buf, count);
	bcm2835_gpio_set(m_csn);
	return count;
}

void NRF24L01P::set_output_power_level(int8_t dBm) {
	uint8_t pwr = RF_PWR_0DBM;
	if (dBm < -12) pwr = RF_PWR_18DBM;
	else if (dBm < -6) pwr = RF_PWR_12DBM;
	else if (dBm < 0) pwr = RF_PWR_6DBM;
	write(RF_SETUP, (RF_DR_2MBPS | pwr));
}
