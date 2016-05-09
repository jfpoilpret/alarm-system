#include "network.hh"

#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>

#include <iostream>

thread_local int Socket::_client_socket;

Socket::Socket(uint16_t port)
{
	_server_socket = socket(AF_INET, SOCK_STREAM, 0);
	sockaddr_in server_addr;
	bzero(&server_addr, sizeof server_addr);
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = INADDR_ANY;
	server_addr.sin_port = htons(port);
	bind(_server_socket, (const sockaddr*) &server_addr, sizeof server_addr);
}

Socket::~Socket()
{
	if (_server_socket > 0) close(_server_socket);
}

void Socket::accept(uint16_t max_connections)
{
	listen(_server_socket, max_connections);
	while (true)
	{
		sockaddr_in client_addr;
		size_t client_len = sizeof client_addr;
		std::cout << "Waiting for client on socket" << std::endl;
		int client_socket = ::accept(_server_socket, (sockaddr*) &client_addr, &client_len);

		if (client_socket > 0)
		{
			std::unique_lock<std::mutex> lock{_threads_mutex};
			std::thread t{&Socket::_process, this, client_socket};
			_threads[t.get_id()] = std::move(t);
		}
	}
}

void Socket::_process(int client_socket)
{
	// Start new thread and pass client_socket
	_client_socket = client_socket;
	std::cout << "Client accepted, processing..." << std::endl;
	process();
	std::cout << "Processing complete." << std::endl;
	close(_client_socket);
	std::unique_lock<std::mutex> lock{_threads_mutex};
	_threads.erase(std::this_thread::get_id());
}

int Socket::read(void* buffer, size_t size)
{
	bzero(buffer, size);
	return ::read(_client_socket, buffer, size);
}

int Socket::write(const void* buffer, size_t size)
{
	return ::write(_client_socket, buffer, size);
}
