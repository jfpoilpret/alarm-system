#ifndef NETWORK_HH
#define	NETWORK_HH

#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>

#include <fstream>
#include <sstream>

const size_t READ_BUFFER_SIZE = 256;

void serve();
void process(int socket);

//class Socket
//{
//public:
//	//TODO
//	// Constructor for server
//	Socket(uint16_t port);
//	// Constructor for client
//	Socket(const std::string& host, uint16_t port);
//	
//	void connect();
//	void disconnect();
//};

#endif	/* NETWORK_HH */

