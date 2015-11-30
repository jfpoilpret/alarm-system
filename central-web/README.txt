Alarm System Central Web Application
====================================

Development (Windows/PyDev)
---------------------------
The application needs python 3.4 installed on the host machine and in the PATH.
Open a command-line window on central-web directory (in this example, Python 3.4 is installed on D:\Python34):
> python d:\Python34\tools\Scripts\pyvenv.py venv
> venv\Scripts\activate
(venv) pip install -r requirements.txt
(venv) pip list
The last command should show the following output:
	aniso8601 (1.0.0)
	dominate (2.1.12)
	Flask (0.10.1)
	Flask-Bootstrap (3.3.5.3)
	Flask-HTTPAuth (2.7.0)
	Flask-RESTful (0.3.4)
	Flask-Script (2.0.5)
	Flask-SQLAlchemy (2.0)
	itsdangerous (0.24)
	Jinja2 (2.7.3)
	MarkupSafe (0.23)
	pip (7.1.2)
	pytz (2015.4)
	pyzmq (14.7.0)
	setuptools (18.2)
	six (1.9.0)
	SQLAlchemy (1.0.0)
	webargs (0.15.0)
	Werkzeug (0.10.4)
	wheel (0.24.0)
	xmltodict (0.9.2)
	
Creating project on Eclipse/PyDev
---------------------------------
	import project into PyDev
	add venv-based python interpreter and ensure that:
		venv and venv\Lib\site-packages are added to the list of libraries
		flask.ext and flask_sqlalchemy are added to forced builtins


TODO
Running the server on Windows (for tests):
First open a command-line window on central-web directory:
> venv\Scripts\activate

Command line operations:

(venv) manage.py -c <config> resetdb
    resets DB (and creates admin/admin user) for DB to use for <config>
    config is one of:
      dev             used for development (port 8080)
      test            used for tests (port 80)
      demo            used for demos (port 8080)
      prod            used for real alarm system (port 80)

(venv) manage.py -c <config> runserver
    runs web service according to <config> settings (different ports and DBs)

Setting up the server on Raspberry Pi
-------------------------------------
Note: The system has been tested on Raspberry Pi 1 Model B+ and 2 Model B without issues.
The following instructions are for Raspbian Jessie Lite:

	- First ensure network setup is finished (WIFI or Ethernet) and system has been updated.
	- install git and python 3.4
		> sudo apt-get install git-core
		> sudo apt-get install python3
		> sudo apt-get install python3-setuptools
		> sudo apt-get install python3-pip
		> sudo apt-get install python3-venv
		> cd (/home/pi)
		> git config --global user.name xxxx
		> git config --global user.email xxxx@yyyy.zzz
		> git clone https://github.com/jfpoilpret/alarm-system.git
		> cd alarm-system/central-web
		> pyvenv venv
		> source venv/bin/activate
		> pip install -r requirements.txt (takes several minutes)
	- then install C dependencies for RFManager module
		> cd
		> wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.46.tar.gz
		> gunzip bcm2835-1.46.tar.gz
		> tar xvf bcm2835-1.46.tar
		> cd bcm2835-1.46
		> ./configure
		> make
		> sudo make check
		> sudo make install
		
		> cd
		> wget https://github.com/jedisct1/libsodium/releases/download/1.0.4/libsodium-1.0.4.tar.gz
		> gunzip libsodium-1.0.4.tar.gz
		> tar xvf libsodium-1.0.4.tar
		> cd libsodium-1.0.4
		> ./configure
		> make
		> make check
		> sudo make install

		> cd
		> wget http://download.zeromq.org/zeromq-4.1.3.tar.gz
		> gunzip zeromq-4.1.3.tar.gz
		> tar xvf zeromq-4.1.3.tar
		> cd zeromq-4.1.3/
		> ./configure
		> make
		> sudo make install
		> sudo ldconfig
		> make check

		> cd /usr/local/include
		> sudo wget https://github.com/zeromq/cppzmq/raw/master/zmq.hpp
		
	- build RFManager for your system
		> cd 
		> cd alarm-system/central-rf/RFManager
		> make

Running the server on Raspberry Pi
----------------------------------

TODO
	- setup initial DB
	- launch RFManager
	- launch central-web

TODO activate venv
$ cd central-web
$ source venv/bin/activate
$ python manage.py -c test resetdb
$ sudo -i
$ cd /home/pi/alarm-system/central-web
$ source venv/bin/activate
$ python manage.py -c test runserver



