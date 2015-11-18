/* 
 * File:   Commands.h
 */

#ifndef COMMANDS_H
#define	COMMANDS_H

#include <string>
#include <istream>

class CommandManager;
class DevicesHandler;
class AlarmStatus;

class Command {
public:
	virtual std::string execute(const std::string& verb, std::istringstream& input) = 0;
	
protected:
	DevicesHandler& handler() const;
	AlarmStatus& status() const;
	void exit();
	void write(const std::string& verb, std::istringstream& input);
	void remove(const std::string& verb);

private:
	CommandManager* manager;
	bool log;
	friend class CommandManager;
};

class InitCommand: public Command {
public:
	static const char* VERB;
	virtual std::string execute(const std::string& verb, std::istringstream& input);
};

class CodeCommand: public Command {
public:
	static const char* VERB;
	virtual std::string execute(const std::string& verb, std::istringstream& input);
};

class StartCommand: public Command {
public:
	static const char* VERB;
	virtual std::string execute(const std::string& verb, std::istringstream& input);
};

class StopCommand: public Command {
public:
	static const char* VERB;
	virtual std::string execute(const std::string& verb, std::istringstream& input);
};

class ExitCommand: public Command {
public:
	static const char* VERB;
	virtual std::string execute(const std::string& verb, std::istringstream& input);
};

class LockCommand: public Command {
public:
	static const char* VERB;
	virtual std::string execute(const std::string& verb, std::istringstream& input);
};

class UnlockCommand: public Command {
public:
	static const char* VERB;
	virtual std::string execute(const std::string& verb, std::istringstream& input);
};

#endif	/* COMMANDS_H */

