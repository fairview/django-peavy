import os

ADMIN_MEDIA_PREFIX = '/static/admin/'
DATABASE_ROUTERS = ['peavy.routers.DjangoDBRouter']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'peavy_demo',
        'USER': 'peavy_demo',
        'PASSWORD': 'peavy_demo',
        'TEST_CHARSET': 'UTF8'
    },
    'peavy': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'peavy_demo',
        'USER': 'peavy_demo',
        'PASSWORD': 'peavy_demo',
        'TEST_CHARSET': 'UTF8'
    }
}
DEBUG = True
DIRNAME = os.path.dirname(__file__)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = (
    'peavy',
    'peavy_demo',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'south',
)

LANGUAGE_CODE = 'en-us'
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
        'peavy': {
            'handlers': ['console', 'peavy'],
            'level':'DEBUG',
        },
        'peavy_demo': {
            'handlers': ['console', 'peavy'],
            'level':'DEBUG',
        },
    }
}
LOGIN_REDIRECT_URL = '/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'peavy.middleware.RequestLoggingMiddleware',
)
ROOT_URLCONF = 'peavy_demo.urls'
SECRET_KEY = 'jj7ck0*b%s)7r7dq%9&#!vvj=w&)3kie=cf_s*=ai43$u4be-v'
SITE_ID = 1
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(DIRNAME, 'static'))
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)
TEMPLATE_DEBUG = True
TIME_ZONE = 'America/New_York'
USE_I18N = True

