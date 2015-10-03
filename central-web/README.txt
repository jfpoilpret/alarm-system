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
	pip (6.0.8)
	pytz (2015.4)
	setuptools (12.0.5)
	six (1.9.0)
	SQLAlchemy (1.0.0)
	webargs (0.15.0)
	Werkzeug (0.10.4)
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

Running the server on Raspberry Pi:
TODO

TODO create venv

TODO activate venv
$ cd central-web
$ source venv/bin/activate
$ python manage.py -c test resetdb
$ sudo -i
$ cd /home/pi/alarm-system/central-web
$ source venv/bin/activate
$ python manage.py -c test runserver



