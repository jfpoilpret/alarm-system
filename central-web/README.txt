Alarm System Central Web Application

First installation:
The application needs python 2.7, pip 1.5, setuptools 6.1 installed on the host machine.
Then, install virtualenv (1.11) with pip.
Open a command-line window on AgendaWebService directory:
> virtualenv venv
> venv\Scripts\activate
(venv) pip install -r requirements.txt
(venv) pip list
The last command should show the following output:
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
