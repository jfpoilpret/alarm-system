Alarm System Central Web Application
====================================

Development (Windows/PyDev)
---------------------------
The application needs python 3.4 installed on the host machine and in the PATH.
Open a command-line window on central-web directory (in this example, Python 3.4 is isntalled on D:\Python34):
> python d:\Python34\tools\Scripts\pyvenv.py venv
> venv\Scripts\activate
(venv) pip install -r requirements-latest.txt
(venv) pip list
The last command should show the following output:
	Flask (0.10.1)
	Flask-Bootstrap (3.3.2.1)
	Flask-Login (0.2.11)
	Flask-Script (2.0.5)
	Flask-SQLAlchemy (2.0)
	Flask-WTF (0.11)
	itsdangerous (0.24)
	Jinja2 (2.7.3)
	MarkupSafe (0.23)
	pip (6.0.8)
	setuptools (12.0.5)
	SQLAlchemy (1.0.0)
	Werkzeug (0.10.4)
	WTForms (2.0.2)
	
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