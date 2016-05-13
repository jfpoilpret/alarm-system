#ifndef CAMERA_HH
#define	CAMERA_HH

#include <Cosa/IOStream.hh>
#include "initializer_list"

class Camera
{
public:
	enum class Resolution
	{
		RES_640x480,
		RES_320x240,
		RES_160x120
	};
	
	enum class BaudRate
	{
		BAUD_9600,
		BAUD_19200,
		BAUD_38400,
		BAUD_57600,
		BAUD_115200,
		// Non official baud rate (to be checked and used with caution)
		BAUD_230400
	};
	
	Camera(IOStream& cam, uint32_t timeout);
	
	void reset();
	template<typename CB> void take_picture(CB& callback);
	void take_picture();
	void stop_picture();
	uint16_t picture_size();
	void picture_content(uint16_t address, uint16_t size, uint8_t* buffer);
	void compression(uint8_t ratio);
	void picture_resolution(Resolution resolution);
	void enter_power_save();
	void exit_power_save();
	void baud_rate(BaudRate baud);
	
private:
	bool _wait_init();
	void _send(std::initializer_list<uint8_t> content);
	bool _receive(std::initializer_list<uint8_t> expected);
	bool _receive(uint8_t* content, uint8_t size);
	void _trace(bool ascii_response = false);

	const uint32_t _timeout;
	IOStream& _cam;
};

#endif	/* CAMERA_HH */

