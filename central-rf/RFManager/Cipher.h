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

#pragma pack()

#endif /* CIPHER_H_ */
