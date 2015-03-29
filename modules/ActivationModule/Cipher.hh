/*
 * Cipher.hh
 *
 *  Created on: 25 janv. 2015
 *      Author: Jean-François
 */

#ifndef CIPHER_HH_
#define CIPHER_HH_

class XTEA
{
public:
	XTEA(const uint8_t rounds = DEFAULT_ROUNDS):_rounds(rounds),_key() {}

	static void generate_key(uint8_t key[4 * 4]);
	void set_key(uint8_t const key[4 * 4]);
	// TODO replace with uint_8t[8]
	void encipher(uint32_t v[2]);
	void decipher(uint32_t v[2]);

	static const size_t KEY_SIZE = 4 * 4;

private:
	static const uint8_t DEFAULT_ROUNDS = 32;
	static const uint32_t KEY_SCHEDULE = 0x9E3779B9;
	const uint8_t _rounds;
	uint32_t const _key[4];
};

void XTEA::generate_key(uint8_t key[KEY_SIZE])
{
	uint32_t* ukey = (uint32_t*) key;
	for (uint8_t i = 0; i < (KEY_SIZE / sizeof(uint32_t)); i++)
		ukey[i] = random();
}

void XTEA::set_key(uint8_t const key[KEY_SIZE])
{
	memcpy((void*) _key, key, KEY_SIZE);
}

void XTEA::encipher(uint32_t v[2])
{
	uint32_t v0 = v[0], v1 = v[1], sum = 0, delta = KEY_SCHEDULE;
	for (uint8_t i = 0; i < _rounds; i++)
	{
		v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + _key[sum & 3]);
		sum += delta;
		v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + _key[(sum>>11) & 3]);
	}
	v[0] = v0;
	v[1] = v1;
}

void XTEA::decipher(uint32_t v[2])
{
	uint32_t v0 = v[0], v1 = v[1], delta = KEY_SCHEDULE, sum = delta * _rounds;
	for (uint8_t i = 0; i < _rounds; i++)
	{
		v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + _key[(sum>>11) & 3]);
		sum -= delta;
		v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + _key[sum & 3]);
	}
	v[0] = v0;
	v[1] = v1;
}

#endif /* CIPHER_HH_ */
