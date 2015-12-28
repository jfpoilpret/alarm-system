#include "Cipher.hh"

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


