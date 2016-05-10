#ifndef NETWORK_HH
#define	NETWORK_HH

#include <list>
#include <unordered_map>
#include <thread>
#include <mutex>

class Socket
{
public:
	// Constructor for server
	Socket(uint16_t port);
	virtual ~Socket();
	
	void accept(uint16_t max_connections = 10);
	void stop(bool wait_for_pending_requests = true);
	
protected:
	virtual void process() = 0;
	int read(void* buffer, size_t size);
	int write(const void* buffer, size_t size);
	
private:
	void _process(int client_socket);

	bool _stop;
	int _server_socket;
	std::unordered_map<std::thread::id, std::thread> _running_threads;
	std::list<std::thread> _finished_threads;
	std::mutex _threads_mutex;
	//TODO add information about client address as thread_local?
	static thread_local int _client_socket;
};

#endif	/* NETWORK_HH */
