============
django-peavy
============

``django-peavy`` is a tool for improving your Django application logging.

Features
--------

* Middleware to tag each request with a unique ID.

* Logging filters to capture request metadata like user, remote IP, and headers.

* Logging handlers for:

  * Capturing exception information, including a copy of the Django server
    error page, in a database.

  * Sending error notifications to admins without revealing sensitive
    information like the contents of request.POST.

* A database router for sending log records to a separate database.

* A simple user interface for browsing log records in the database.

Installation
------------

Start with Django 1.3 or higher; peavy is intended for use with the new logging
configuration first available in that version.

To install, simply run::

    pip install django-peavy

Configuration
-------------

1. Add ``peavy`` to your ``INSTALLED_APPS`` setting.

2. To avoid interfering with your application's database transactions, peavy
   logs to its own database by default.

   The easiest way to make this work is to create a second database
   stanza in settings.DATABASES, that mirrors the default settings under
   another name, e.g.::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'defaultdb',
            'USER': 'dbuser',
            'PASSWORD': 'dbpassword,
            'TEST_CHARSET': 'UTF8'
        },
        'peavy': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'defaultdb',
            'USER': 'dbuser',
            'PASSWORD': 'dbpassword,
            'TEST_CHARSET': 'UTF8'
        }
    }

   This should get your tables created/migrated properly, and allow peavy to
   work with its own connection to the database. When it commits log entries,
   your application's transactions won't be affected.

   If you want to use a name other than 'peavy' for the peavy database, it
   needs to be specified in settings.PEAVY_DATABASE_NAME.

   If you want to put peavy in a truly separate database, you can still use
   South by specifying both app and database when running peavy migrations::

      $ django-admin.py migrate peavy --database=peavy

   If you omit the app name, you will probably encounter errors with other apps
   whose migrations South tries to run.

   Finally, you can use a separate database but tell South to ignore it
   completely by adding this to your settings::

       SOUTH_MIGRATION_MODULES = {
           'peavy': 'ignore',
       }

   In this case, you'll just create peavy's tables with syncdb.

3. Add the peavy database router::

    DATABASE_ROUTERS = ['peavy.routers.DjangoDBRouter']

4. Add the logging configuration. For example::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '[%(asctime)s %(name)s %(levelname)s] %(message)s'
            },
            'basic': {
                'format': '[%(asctime)s %(uuid)s %(user)s %(name)s %(levelname)s] %(message)s'
            },
            'meta': {
                'format': '[%(asctime)s %(client_ip)s %(uuid)s %(user)s %(name)s %(levelname)s] %(message)s'
            },
        },
        'filters': {
            'basic': {
                '()': 'peavy.filters.BasicFilter',
            },
            'meta': {
                '()': 'peavy.filters.MetaFilter',
            }
        },
        'handlers': {
            'null': {
                'level':'DEBUG',
                'class':'django.utils.log.NullHandler',
            },
            'console': {
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'filters': ['basic', 'meta'],
                'formatter': 'basic'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'peavy.handlers.AdminEmailHandler',
                'filters': ['basic', 'meta'],
                'formatter': 'meta'
            },
            'peavy': {
                'level': 'INFO',
                'class': 'peavy.handlers.DjangoDBHandler',
                'filters': ['basic', 'meta'],
                'formatter': 'meta'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['null'],
                'propagate': True,
                'level':'INFO',
            },
            'django.request': {
                'handlers': ['peavy', 'mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'myapp': {
                'handlers': ['console', 'peavy'],
                'level':'DEBUG',
            }
        }
    }

5. Add ``peavy.middleware.RequestLoggingMiddleware`` to MIDDLEWARE_CLASSES.

6. Add ``django.core.context_processors.request`` to TEMPLATE_CONTEXT_PROCESSORS.

7. Run ``manage.py migrate`` to create the database tables, or if you're really
   logging to a second database and have disabled South migrations for peavy,
   run ``manage.py syncdb``.

The last two steps can be skipped if you don't want the UI.

8. If desired, add ``peavy.urls`` to your URL configuration to get the UI::

    urlpatterns += patterns('',
        (r'^peavy/', include('peavy.urls', namespace='peavy')),
    )

9. Run ``manage.py collectstatic`` to copy peavy's media into place.

Demo Application
----------------

Peavy comes with an example application that demonstrates how to log with it,
and lets you check out the UI. To run it:

1. Create a virtualenv for it, then activate the virtualenv.

2. Copy the example application from your copy of django-peavy into the virtualenv::

   $ rsync -av peavy_demo/ $VIRTUAL_ENV/peavy_demo/

3. Install its requirements with pip::

   $ pip install -r $VIRTUAL_ENV/peavy_demo/requirements.txt

4. Set up the PostgreSQL database to match the Django settings. You can of
   course use another database, but it has to support concurrent transactions
   (so sqlite is out), and you'll have to adjust the settings and install the
   adapter yourself.

5. Adjust your PYTHONPATH to pick up the demo app::

   $ export PYTHONPATH=$VIRTUAL_ENV:$PYTHONPATH

6. Set the DJANGO_SETTINGS_MODULE environment variable::

   $ export DJANGO_SETTINGS_MODULE=peavy_demo.settings

7. Run 'django-admin syncdb' to populate the database and create a superuser.

8. Run 'django-admin migrate' to create peavy's tables.

9. Run the devserver::

   $ django-admin.py runserver

10. Browse to http://localhost:8000/, enter a movie quote, then check the logging
    at http://localhost:8000/peavy/.

Notes
-----

Q. Why "peavy"?
A. See http://en.wikipedia.org/wiki/Peavey_%28tool%29. It's a lumberjack tool,
and it's OK. Oh, come on, it's *required*.

Future
------

* support for logging to other sinks: message queues, non-relational databases.

