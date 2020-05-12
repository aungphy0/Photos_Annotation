# Photos Annotation App

If Django is not installed yet on your machine, please install it by following command
- sudo pip3 install -U django==2.2.12

Install all these libraries
- pip3 install Pillow
- pip3 install gpsphoto
- pip3 install exifread
- pip3 install piexif
- pip3 install geopy

Install mysqlclient
- pip3 install mysqlclient

sudo pip3 install mysqlclient fails with mysql_config not found
- sudo pip3 install libmysqlclient-dev

if still get error please try this
- sudo pip3 install python3.5-dev libmysqlclient-dev

if still get error please try this
- sudo pip3 install python3.6-dev libmysqlclient-dev

And then install mysqlclient
- sudo pip3 install mysqlclient

Create the database in mysql
- mysql -u root -p
- create database Metadata

Setup database please go to project864/settings.py

DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'Metadata',
          'USER': 'root',
          'PASSWORD': 'your_mysql_database_password'
      }
}

Migration and connecting to DB
- python3 manage.py makemigrations annotateApp

you will see something like this
- annotateApp/migrations/0003_auto_20200512_0556.py

And then run the following command
- python3 manage.py migrate

you will see something like this
- Operations to perform:
- Apply all migrations: admin, annotateApp, auth, contenttypes, sessions

You are all set for the database connection!

To run the application
- python3 manage.py runserver

To test the application
- go to the browser and type localhost:8000
