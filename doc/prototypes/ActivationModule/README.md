The ActivationModule prototype is based on:

- Arduino UNO
- Keypad 3x4
- NRF24L01
- 3 LED (Red, Green, Yellow)

The principles are as follow:

1. On reset, the module registers itself with the Alarm center. If registration fails (alarm center does not respond), then registration will be retried every minute until it works. Registration notifies the module of its ID, and the current alarm status (either standby or off). Then power settings are configured to limit current consumption.
2. Once registered, the module scans the keypad every 64ms. Code input is buffered until either '*' (lock) or '#' (unlock) is typed. Once a code is typed, it is encrypted with the latest key received from the center, and then sent to the center. The alarm responds with either Locked, Unlocked or Bad code.
3. Every minute, the module signals itself to the alarm center. In particular, it notifies its voltage level. In response, the alarm center return a new key to be used for encryption of codes.
4. 3 LEDs are lit based on the following scheme:
	- RED: access is forbidden (alarm is locked)
	- GREEN: access is allowed (alarm is unlocked)
	- YELLOW: every time a key is typed on the keypad

The wiring of the prototype is quite straightforward:
	- D1,D3-D8: used for keypad connection
	- D2,D9-D13: used by NRF24L01
	- A0: used by RED LED
	- A1: used by GREEN LED
	- A2: used by YELLOW LED
	
Here are the resistor values for each LED (~5mA) for 5V basic voltage:
	http://www.hacktronics.com/Tools/led-resistor-calculator.html
	
	RED & YELLOW:	Vf = 2.0-2.3V	=> 680 Ohms
	GREEN:			Vf = 3.2V-3.4V 	=> 330 Ohms

Note that on the final module circuit, resistors value shall be changed according to actual voltage supply (probably 3V)
	
	