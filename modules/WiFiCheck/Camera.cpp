#include "Camera.hh"
#include <Cosa/RTT.hh>
#include <Cosa/Trace.hh>

static const size_t CAM_RECV_BUFFER_SIZE = 16;
static const size_t CAM_PICT_BUFFER_SIZE = 64;

static uint8_t HI(uint16_t in)
{
	return (in >> 8);
}

static uint8_t LO(uint16_t in)
{
	return (in & 0xFF);
}

static uint16_t SWAP(uint16_t in)
{
	return (LO(in) << 8) | HI(in);
}

Camera::Camera(IOStream& cam, uint32_t timeout, bool debug)
	: _cam(cam), _timeout(timeout * 1000), _debug(debug)
{
	reset();
}

void Camera::reset()
{
	if (_debug)
		trace << "reset" << endl;
	_send({0x56, 0x00, 0x26, 0x00});
	_receive({0x76, 0x00, 0x26, 0x00, 0x00});
	// Reset generates the power on init string: wait until it is received
//		_wait_init();
	delay(3000);
	_cam.device()->empty();
		_trace(true);
}

template<typename CB>
void Camera::take_picture(CB& callback)
{
	take_picture();
	int32_t size = picture_size();
	uint16_t address = 0;
	while (size > 0)
	{
		//TODO buffer should be an argument to the function (more customizable)
		uint8_t buffer[CAM_PICT_BUFFER_SIZE];
		picture_content(address, CAM_PICT_BUFFER_SIZE, buffer);
		address += CAM_PICT_BUFFER_SIZE;
		size -= CAM_PICT_BUFFER_SIZE;
		callback(buffer, CAM_PICT_BUFFER_SIZE, (size > 0));
	}
	stop_picture();
}

void Camera::take_picture()
{
	if (_debug)
		trace << "take_picture" << endl;
	_send({0x56, 0x00, 0x36, 0x01, 0x00});
	_receive({0x76, 0x00, 0x36, 0x00, 0x00});
}

void Camera::stop_picture()
{
	if (_debug)
		trace << "stop_picture" << endl;
	_send({0x56, 0x00, 0x36, 0x01, 0x03});
	_receive({0x76, 0x00, 0x36, 0x00, 0x00});
}

uint16_t Camera::picture_size()
{
	if (_debug)
		trace << "get picture_size" << endl;
	_send({0x56, 0x00, 0x34, 0x01, 0x00});
	uint16_t size;
	if (	_receive({0x76, 0x00, 0x34, 0x00, 0x04, 0x00, 0x00})
		&&	_receive((uint8_t*)(&size), sizeof(size)))
		return SWAP(size);
	return 0;
}

void Camera::picture_content(uint16_t address, uint16_t size, uint8_t* buffer)
{
	_send({
		0x56, 0x00, 0x32, 0x0C, 0x00, 0x0A, 
		0x00, 0x00, HI(address), LO(address), 
		0x00, 0x00, HI(size), LO(size), 
		0x00, 0x0A});
	_receive({0x76, 0x00, 0x32, 0x00, 0x00}) &&
	_receive(buffer, size) &&
	_receive({0x76, 0x00, 0x32, 0x00, 0x00});
}

void Camera::compression(uint8_t ratio)
{
	if (_debug)
		trace << "compression" << endl;
	_send({0x56, 0x00, 0x31, 0x05, 0x01, 0x01, 0x12, 0x04, ratio});
	_receive({0x76, 0x00, 0x31, 0x00, 0x00});
}

void Camera::picture_resolution(Resolution resolution)
{
	if (_debug)
		trace << "picture_resolution" << endl;
	uint8_t code = 0x00;
	switch (resolution)
	{
		case Resolution::RES_160x120: code = 0x22; break;
		case Resolution::RES_320x240: code = 0x11; break;
		case Resolution::RES_640x480: code = 0x00; break;
	}
	_send({0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19, code});
	_receive({0x76, 0x00, 0x31, 0x00, 0x00});
}

void Camera::enter_power_save()
{
	if (_debug)
		trace << "enter_power_save" << endl;
	_send({0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x01});
	_receive({0x76, 0x00, 0x3E, 0x00, 0x00});
}

void Camera::exit_power_save()
{
	if (_debug)
		trace << "exit_power_save" << endl;
	_send({0x56, 0x00, 0x3E, 0x03, 0x00, 0x01, 0x00});
	_receive({0x76, 0x00, 0x3E, 0x00, 0x00});
}

void Camera::baud_rate(BaudRate baud)
{
	if (_debug)
		trace << "baud_rate" << endl;
	uint16_t code = 0x2AF2;
	switch (baud)
	{
		case BaudRate::BAUD_9600: code = 0xAEC8; break;
		case BaudRate::BAUD_19200: code = 0x56E4; break;
		case BaudRate::BAUD_38400: code = 0x2AF2; break;
		case BaudRate::BAUD_57600: code = 0x1C4C; break;
		case BaudRate::BAUD_115200: code = 0x0DA6; break;
		// Non official baud rate (to be checked and used with caution)
		// I inferred this formula to calculate value from baud rate:
		//		code = 432'000'000/baud - 256
		case BaudRate::BAUD_230400: code = 0x0653; break;
	}
	_send({
		0x56, 0x00, 0x24, 0x03, 0x01, 
		HI(code), LO(code)});
	_receive({0x76, 0x00, 0x24, 0x00, 0x00});
}
	
bool Camera::_wait_init()
{
	// Wait until timeout or expected received
	uint32_t now = RTT::millis();
	do
	{
		char buffer[80];
		if (	_cam.readline(buffer, sizeof(buffer), false)
			&&	strstr(buffer, "Init end"))
		{
			_cam.device()->empty();
			return true;
		}
		delay(1);
	}
	while (RTT::since(now) < 3000);
	if (_debug)
		trace << "wait init timeout." << endl;
	_cam.device()->empty();
	return false;
}

void Camera::_send(std::initializer_list<uint8_t> content)
{
	for (auto i : content)
		_cam.device()->putchar(i);
	_cam.device()->flush();
}

bool Camera::_receive(std::initializer_list<uint8_t> expected)
{
	uint8_t content[CAM_RECV_BUFFER_SIZE];
	if (_receive(content, expected.size()))
	{
		uint8_t* compare = content;
		for (auto i : expected)
		{
			if (*compare != i)
			{
				if (_debug)
					trace << "expected " << hex << i << ", actual " << hex << *compare << endl;
				return false;
			}
			++compare;
		}
		return true;
	}
	return false;
}

bool Camera::_receive(uint8_t* content, uint8_t size)
{
	// Wait until timeout or expected received
	uint32_t now = RTT::millis();
	uint8_t count = 0;
	do
	{
		while (_cam.device()->available())
		{
			*content++ = _cam.device()->getchar();
			if (++count == size)
				return true;
		}
		delay(1);
	}
	while (RTT::since(now) < _timeout);
	if (_debug)
		trace << "receive timeout. Expected size " << size << ", actual " << count << endl;
	return false;
}

void Camera::_trace(bool ascii_response)
{
	if (_debug)
	{
		trace << "<< ";
		while (_cam.device()->available()) 
		{
			int c = _cam.device()->getchar();
			if (ascii_response)
				trace << (char) c;
			else
				trace << hex << c << ' ';
		}
		trace << endl;
	}
}
