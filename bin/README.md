This directory contains a few shell scripts that are useful:
- for development
- for alarm system execution

It is advised to create symbolic links, in your home directory, to these scripts and call them when needed. Most scripts should be called through `sudo`.

Scripts expect the following location for the alarm system:

> /home/pi/alarm-system

Several scripts are available:

- `command` is used  to simulate a command to `RFManager`
- `listen` is used to listen to all messages sent by `RFManager` and store them on local directory to `data.log`
- `listen2` is used to listen to all messages sent by `RFManager` and display them to standard output
- `rfm` launches `RFManager`
- `resetdb` cleans up the database of the alarm system (for the given configuration) and initializes it with the admin user
- `runserver` executes the alarm system web server for the given configuration
