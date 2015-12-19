Alarm System Central Web Application - AVR-based Modules
========================================================

All modules can be built and uploaded as netbeans 8.0 projects.
Compilation of any module has some setup pre-requisites.

Toolchain
---------
Netbeans setup needs AVR toolchain which is available from standard Arduino IDE install.
I currently use Arduino 1.6.6 on Windows 8.1 but any recent Arduino version on any Operating System should work fine.

Netbeans also needs the make utility (standard on Linux systems) which you will have to install yourself if you use Windows. Make was present in Arduino distributions until 1.5.8 but has been removed since.
You can use make from Cygwin, MSYS (I use MSYS64), or directly from GNU (http://gnuwin32.sourceforge.net/packages/make.htm).


Cosa library installation
-------------------------
All modules are based on Cosa library (https://github.com/mikaelpatel/Cosa) which you need to install on your computer. You may clone the original git repository or just install a ZIP (TODO version). Whatever way you choose, it is advised to install the library at the same level as the alarm-system location; this is where netbeans projects are configured to look for.

Netbeans Tools setup
----------------------


Project Configurations
----------------------


Build & Upload
----------------------


