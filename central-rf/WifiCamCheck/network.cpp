#include "network.hh"

#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>

#include <iostream>

thread_local int Socket::_client_socket;

const int32_t SELECT_TIMEOUT = 1;

Socket::Socket(uint16_t port):_stop(false)
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

void Socket::stop(bool wait_for_pending_requests)
{
	// Signal accept() to stop waiting for connections
	_stop = true;
	if (wait_for_pending_requests)
	{
		// Wait for all current threads to terminate normally
		std::unique_lock<std::mutex> lock{_threads_mutex};
		for (auto& t: _finished_threads)
			t.join();
		_finished_threads.clear();
		for (auto& t: _running_threads)
			t.second.join();
		_running_threads.clear();
	}
}

void Socket::accept(uint16_t max_connections)
{
	_stop = false;
	listen(_server_socket, max_connections);
	std::cout << "Waiting for client on socket" << std::endl;
	while (true)
	{
		timeval timeout;
		timeout.tv_sec = SELECT_TIMEOUT;
		timeout.tv_usec = 0;
		fd_set set;
		FD_ZERO(&set);
		FD_SET(_server_socket, &set);
		
		int result = select(FD_SETSIZE, &set, 0, 0, &timeout);

		// First check if we must stop here
		if (_stop)
			break;
		
		if (result > 0)
		{
			sockaddr_in client_addr;
			size_t client_len = sizeof client_addr;
			int client_socket = ::accept(_server_socket, (sockaddr*) &client_addr, &client_len);

			if (client_socket > 0)
			{
				std::unique_lock<std::mutex> lock{_threads_mutex};
				std::thread t{&Socket::_process, this, client_socket};
				_running_threads[t.get_id()] = std::move(t);
				
				//TODO Do this everytime but based on some atomic bool value to avoid extra lock every second?
				for (auto& t: _finished_threads)
					t.join();
				_finished_threads.clear();
			}
		}
		if (result != 0)
			std::cout << "Waiting for client on socket" << std::endl;
	}
}

//TODO Add processing time...
void Socket::_process(int client_socket)
{
	// Start new thread and pass client_socket
	_client_socket = client_socket;
	std::cout << "Client accepted, processing..." << std::endl;
	process();
	std::cout << "Processing complete." << std::endl;
	close(_client_socket);
	std::unique_lock<std::mutex> lock{_threads_mutex};
	_finished_threads.push_back(std::move(_running_threads[std::this_thread::get_id()]));
	_running_threads.erase(std::this_thread::get_id());
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
