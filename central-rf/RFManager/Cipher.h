/*
 * Cipher.h
 */

#ifndef CIPHER_H_
#define CIPHER_H_

#include <cstdlib>
#include <stdint.h>

#pragma pack(1)

class XTEA
{
public:
	static const size_t KEY_SIZE = 4 * 4;

	XTEA(const uint8_t rounds = DEFAULT_ROUNDS):_rounds(rounds),_key() {}
	XTEA(const XTEA& rhs);
	XTEA& operator = (const XTEA& rhs);

	static void generate_key(uint8_t key[KEY_SIZE]);
	void set_key(uint8_t const key[KEY_SIZE]);

	void encipher(uint32_t v[2]);
	void decipher(uint32_t v[2]);

private:
	static const uint8_t DEFAULT_ROUNDS = 32;
	static const uint32_t KEY_SCHEDULE = 0x9E3779B9;
	uint8_t _rounds;
	uint32_t const _key[KEY_SIZE / sizeof(uint32_t)];
};

#pragma pack()

#endif /* CIPHER_H_ */
