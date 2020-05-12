# Photos Annotation App

If Django is not installed yet on your machine, please install it by following command
- sudo pip3 install -U django==2.2.12

Install mysqlclient
- pip3 install mysqlclient

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
annotateApp/migrations/0003_auto_20200512_0556.py

And then run the following command
- python3 manage.py migrate
