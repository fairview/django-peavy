============
django-peavy
============

``django-peavy`` is a collection of support code and a basic user interface to
facilitate capturing your Django logging to a database. It's intended for use
with the new logging configuration in Django 1.3.

Features
--------

* Middleware to tag each request with a unique ID.

* Logging filters to capture request metadata like user, remote IP, and headers.

* Logging handlers for:

  * Capturing exception information, including a copy of the Django server
    error page, in a database.

  * Sending error notifications to admins without revealing sensitive
    information like the contents of request.POST.

* A database router for sending log records to a separate database (though
  there are problems with South migrations you'll need to work around to do
  so).

* A simple user interface for browsing log records in the database.

Installation
------------

To install, simply run::

    pip install django-peavy

Configuration
-------------

1. Add ``peavy`` to your ``INSTALLED_APPS`` setting.

2. Run ``manage.py migrate`` to create the database tables.

3. Add the logging configuration to settings.py. For example::

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
         
4. Add ``peavy.middleware.RequestLoggingMiddleware`` to MIDDLEWARE_CLASSES.

The last two steps can be skipped if you don't want the UI.

5. If desired, add ``peavy.urls`` to your URL configuration to get the UI::

    urlpatterns += patterns('',
        (r'^peavy/', include('peavy.urls')),
    )

6. Run ``manage.py collectstatic`` to copy peavy's media into place.

Notes
-----

Q. Why "peavy"?
A. See http://en.wikipedia.org/wiki/Peavey_%28tool%29. It's a lumberjack tool,
and it's OK. Oh, come on, it's *required*.

Future
------

* Adding search to the UI.
* Possibly, support for logging to non-relational databases.

