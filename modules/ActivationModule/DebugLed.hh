/*
 * DebugLed.hh
 *
 *  Created on: 12 févr. 2015
 *      Author: Jean-François
 */

#ifndef DEBUGLED_HH_
#define DEBUGLED_HH_

#ifdef DEBUGLED_ENABLED
#include <Cosa/OutputPin.hh>

extern OutputPin ledOutput;

void debug(uint8_t blinks = 1, uint16_t us = 200)
{
	for (uint8_t i = 0; i < blinks; i++)
	{
		ledOutput.on();
		DELAY(us);
		ledOutput.off();
		DELAY(us);
	}
}
#endif

#endif /* DEBUGLED_HH_ */
