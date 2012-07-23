# Django settings for barbaris project.
# -*- coding: utf-8 -*-
###############################################################################
# Copyright 2012 Grigoriy Kramarenko.
###############################################################################
# This file is part of Barbaris.
#
#    Barbaris is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Barbaris is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Barbaris.  If not, see <http://www.gnu.org/licenses/>.
#
# Этот файл — часть Barbaris.
#
#   Barbaris - свободная программа: вы можете перераспространять ее и/или
#   изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
#   в каком она была опубликована Фондом свободного программного обеспечения;
#   либо версии 3 лицензии, либо (по вашему выбору) любой более поздней
#   версии.
#
#   Barbaris распространяется в надежде, что она будет полезной,
#   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
#   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
#   общественной лицензии GNU.
#
#   Вы должны были получить копию Стандартной общественной лицензии GNU
#   вместе с этой программой. Если это не так, см.
#   <http://www.gnu.org/licenses/>.
###############################################################################


from django.utils.translation import ugettext_lazy as _
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
def abspath(*paths):
    return os.path.abspath(os.path.join(PROJECT_PATH, *paths)).replace('\\','/')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': abspath('data.sqlite'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Vladivostok'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = abspath('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = abspath('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p_u(d)es4q)d!x!ajft5sx3q#hjc3c)x%=j4rd+k!o&amp;*#%_+0d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'barbaris.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'barbaris.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    abspath("templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # append:
    'django.core.context_processors.request'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'barbaris.online',
    'barbaris.auth_fix',
    'cachebot',
    'memcache_status',
)

# Settings for applications:

START_YEAR = 2011

STATE_ORDER_CREATE   = 1
STATE_ORDER_RESERV   = 2
STATE_ORDER_ACCEPT   = 3
STATE_ORDER_CLOSE    = 4
STATE_ORDER_CANCEL   = 5
STATE_ORDER_CHOICES = (
        (STATE_ORDER_CREATE, u'Создан'),
        (STATE_ORDER_RESERV, u'Бронь'),
        (STATE_ORDER_ACCEPT, u'Принят'),
        (STATE_ORDER_CLOSE,  u'Закрыт'),
        (STATE_ORDER_CANCEL, u'Отменён'),
    )
SELECT_WORK_ORDERS = [1,2,3]

STATE_INVOICE_CREATE   = 1
STATE_INVOICE_PAYMENT  = 2
STATE_INVOICE_CANCEL   = 3
STATE_INVOICE_CHOICES = (
        (STATE_INVOICE_CREATE, u'Создан'),
        (STATE_INVOICE_PAYMENT, u'Оплачен'),
        (STATE_INVOICE_CANCEL, u'Отменён'),
    )
SELECT_INVOICES = [1,2,3]

PAYMENT_INVOICE_CASH      = 1
PAYMENT_INVOICE_CASHLESS  = 2
PAYMENT_INVOICE_CARD      = 3
PAYMENT_INVOICE_CHOICES = (
        (PAYMENT_INVOICE_CASH,     u'Наличный'),
        (PAYMENT_INVOICE_CASHLESS, u'Безналичный'),
        (PAYMENT_INVOICE_CARD,     u'Карта банка'),
    )

ATTRIBUTE_WEDDING    = 1
ATTRIBUTE_SPORTSMANS = 2
ATTRIBUTE_CHOICES = (
        (ATTRIBUTE_WEDDING, u'Свадьба'),
        (ATTRIBUTE_SPORTSMANS, u'Спортсмены'),
    )

DIVIDER_DAY   = 1
DIVIDER_HOUR  = 2
DIVIDER_MONTH = 3
DIVIDER_PRICE_CHOICES = (
        (DIVIDER_DAY, u'Сутки'),
        (DIVIDER_HOUR, u'Час'),
        (DIVIDER_MONTH, u'Месяц'),
    )

CATEGORY_CHOICES = (
        (u'Hotel',u'Гостиница'),
        (u'Sauna',u'Сауна'),
        (u'Kitchen',u'Кухня'),
        (u'Parking',u'Автостоянка'),
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        #~ 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'BACKEND': 'cachebot.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'barbaris',
    }
}
