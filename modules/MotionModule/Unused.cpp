
#include <Cosa/Wireless.hh>
#include <NRF24L01P.hh>
#include <Cosa/Job.hh>
#include <Cosa/ExternalInterrupt.hh>
#include <Cosa/PinChangeInterrupt.hh>

// The following virtual methods are inline hence not overridable here...
//void Wireless::Driver::wakeup_on_radio() {}
//bool Wireless::Driver::room() {return false;}
//int Wireless::Driver::broadcast(uint8_t port, const iovec_t* vec) {return 0;}
//int Wireless::Driver::broadcast(uint8_t port, const void* buf, size_t len) {return 0;}
//bool Wireless::Driver::is_broadcast() {return false;}
//int Wireless::Driver::input_power_level() {return 0;}
//int Wireless::Driver::link_quality_indicator() {return 0;}
//bool NRF24L01P::end() {return false;}

// The followinf methods are not inline, thus can be overridden here/ this compiles! But not links...
//void NRF24L01P::powerup() {}
//void NRF24L01P::powerdown() {}
//
//bool Job::Scheduler::stop(Job* job) {return false;}
//
//void ExternalInterrupt::enable() {}
//void ExternalInterrupt::disable() {}
//void ExternalInterrupt::clear() {}
//
//void PinChangeInterrupt::disable() {}
