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

2. Add the peavy database router::

    DATABASE_ROUTERS = ['peavy.routers.DjangoDBRouter']

3. Create a dedicated database for logging.

   If you want to name it something other than 'peavy', you'll need to specify
   it in ``settings.PEAVY_DATABASE_NAME``.

   The separate database makes schema management a little trickier than usual.
   It needs to contain South's migration history table as well as Peavy's log
   records.

   So first, run syncdb on your default database::

      $ django-admin.py syncdb
   
   And of course if you have other apps using South, migrate them::

      $ django-admin.py migrate

   This will actually create peavy tables in your default database. Sorry for
   the debris; South isn't yet obeying database routers.
   
   Now on to peavy's database::

      $ django-admin.py syncdb --database=peavy

   Then run Peavy's South migrations::

      $ django-admin.py migrate peavy --database=peavy

   (Of course, if you chose a different name for the database, use that in
   these last two commands.)

   If you omit the app name, you may encounter errors with other apps whose
   migrations South tries to run.

4. Add the logging configuration. For example::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '[%(asctime)s %(name)s %(levelname)s] %(message)s'
            },
            'basic': {
                'format': '[%(asctime)s %(uuid)s %(user_pk)s:%(username)s %(name)s %(levelname)s] %(message)s'
            },
            'meta': {
                'format': '[%(asctime)s %(client_ip)s %(uuid)s %(user_pk)s:%(username)s %(name)s %(levelname)s] %(message)s'
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

The last two steps can be skipped if you don't want the UI.

7. If desired, add ``peavy.urls`` to your URL configuration to get the UI::

    urlpatterns += patterns('',
        (r'^peavy/', include('peavy.urls', namespace='peavy')),
    )

8. Run ``manage.py collectstatic`` to copy peavy's media into place.

Demo Application
----------------

Peavy comes with an example application that demonstrates how to log with it,
and lets you check out the UI. To run it:

1. Create a virtualenv for it, then activate the virtualenv.

2. Copy the example application from your copy of django-peavy into the virtualenv::

   $ rsync -av peavy_demo/ $VIRTUAL_ENV/peavy_demo/

3. Install its requirements with pip::

   $ pip install -r $VIRTUAL_ENV/peavy_demo/requirements.txt

4. Set up the PostgreSQL databases to match the Django settings (see step 2
   under Configuration, above). You can of course use another database, but it
   has to support concurrent transactions (so sqlite is out), and you'll have
   to adjust the settings and install the adapter yourself.

5. Adjust your PYTHONPATH to pick up the demo app::

   $ export PYTHONPATH=$VIRTUAL_ENV:$PYTHONPATH

6. Set the DJANGO_SETTINGS_MODULE environment variable::

   $ export DJANGO_SETTINGS_MODULE=peavy_demo.settings

7. Run the devserver::

   $ django-admin.py runserver

8. Browse to http://localhost:8000/, enter a movie quote, then check the logging
    at http://localhost:8000/peavy/.

Notes
-----

Q. Why "peavy"?
A. See http://en.wikipedia.org/wiki/Peavey_%28tool%29. It's a lumberjack tool,
and it's OK. Oh, come on, it's *required*.

Future
------

* support for logging to other sinks: message queues, non-relational databases.
