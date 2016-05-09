/* 
 * File:   main.cpp
 *
 * Main entry point of Alarm System central process to communicate to sensor devices through NRF24L01 chip.
 * This process is used to communicate with all devices and proxy all exchanges from/to the web system 
 * on Raspbery Pi (Python-based).
 */

#include "network.hh"

#include <iostream>
#include <fstream>
#include <sstream>

const size_t READ_BUFFER_SIZE = 256;
const uint16_t LISTENING_PORT = 9999;

class PictureServer: public Socket
{
public:
	PictureServer():Socket(LISTENING_PORT){}

protected:
	virtual void process()
	{
		static uint32_t index = 0;

		std::ostringstream file;
		file << "camera-" << ++index << ".jpg";
		std::ofstream output(file.str(), std::ofstream::trunc | std::ofstream::binary);
		while (true)
		{
			char buffer[READ_BUFFER_SIZE];
			int n = read(buffer, READ_BUFFER_SIZE);
			if (n <= 0)
				break;
			output.write(buffer, n);
		}
		output.close();
	}
};

int main(int argc, char** argv)
{
	PictureServer server;
	server.accept();
	return 0;
}
