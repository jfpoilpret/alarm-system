#include "network.hh"
#include <iostream>

void process(int socket)
{
	static uint32_t index = 0;
	
	std::ostringstream file;
	file << "camera-" << ++index << ".jpg";
	std::ofstream output(file.str(), std::ofstream::trunc | std::ofstream::binary);
	while (true)
	{
		char buffer[READ_BUFFER_SIZE];
		bzero(buffer, READ_BUFFER_SIZE);
		int n = read(socket, buffer, READ_BUFFER_SIZE);
//		std::cout << "Read " << n << " bytes." << std::endl;
		if (n <= 0)
			break;
		
		output.write(buffer, n);
	}
	output.close();
}

void serve()
{
	int server_socket = socket(AF_INET, SOCK_STREAM, 0);
	sockaddr_in server_addr;
	bzero(&server_addr, sizeof server_addr);
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = INADDR_ANY;
	server_addr.sin_port = htons(9999);
	bind(server_socket, (const sockaddr*) &server_addr, sizeof server_addr);
	listen(server_socket, 10);
	while (true)
	{
		sockaddr_in client_addr;
		size_t client_len = sizeof client_addr;
		std::cout << "Waiting for client on socket" << std::endl;
		int client_socket = accept(server_socket, (sockaddr*) &client_addr, &client_len);
		std::cout << "Client accepted, processing..." << std::endl;
		process(client_socket);
		std::cout << "Processing complete." << std::endl;
	}
	
}


