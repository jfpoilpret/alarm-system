/* 
 * File:   Commands.h
 */

#ifndef COMMANDS_H
#define	COMMANDS_H

#include "RFManager.h"

//TODO add logging here also and complete handling of config files

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

