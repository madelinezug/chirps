# chirps3.0
A secure re-make of the Pomona Chirps announcement section for System Security, Fall 2018

original website created by Sarah Jin, Maddie Zug, Mark Penrod for Database Systems, Spring 2018

Before everything else, clone the repo:
Git clone https://github.com/madelinezug/chirps.git

Django is a Python-based web framework. Commands to run in terminal are pink. Django Intro

First, Install Homebrew if you don’t have it.

Then it’s easy to install python 3 by running this command in terminal:
> brew install python3

This will install pip3 automatically.

Install virtualEnv 
(These all came from this tutorial on contributing to the Django open source project)
VirtualEnv for Python - This will keep things clean. Basically it lets you have one version of python installed for one project and another for another project.
> pip3 install virtualenv
Make a directory for your virtual environments and create a “djangodev” environment.
> mkdir ~/.virtualenvs
> python3 -m venv ~/.virtualenvs/djangodev
Activate your virtual environment
> source ~/.virtualenvs/djangodev/bin/activate

Now we can get back to Django Database Installation- for doing more than just mySQLLite (which we’ll need. I’m starting with MySQL for now but we’ll have to figure out what DB is best for us.) Django needs MySQL 5.5 or higher. 
To install Django code make sure your virtual environment is activated and type:
> pip install Django
To check that everything worked:
> python -m django --version


Getting the SQL server set up
Follow instructions at: https://dev.mysql.com/doc/mysql-getting-started/en/
After installing the SQL .dmg package, be sure to add it to your path by typing in terminal:
> export PATH=${PATH}:/usr/local/mysql/bin
To turn on the mySQL service pane go to System Preferences and open the mySQL icon (after you have mySQL installed)

Install mysqlclient
> pip install mysqlclient


Specific notes for mySQL
https://docs.djangoproject.com/en/2.0/ref/databases/#mysql-notes

You’ll have to set up your own username and password. Keep track of it :) 

In your project directory navigate to chirps/chirps/settings and replace this:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chirps',
        'USER': '',
        'PASSWORD':'',
        'HOST': '',
        'PORT': ''
    }
}

To reflect your sql username and password.

A resource:
http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django


To see the website make sure your virtual environment is activated and use this command to start a local server:
> Python manage.py runserver

And navigate to this url: http://127.0.0.1:8000/accounts/login/



