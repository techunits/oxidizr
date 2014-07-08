"""
Django settings for oxidizr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kvz5_p1_qtl3g_yit(g7s*142n1fx8sarprj3rvmm9wdokeh3i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['oxidizr.com', 'oxr.local']


# Application definition

INSTALLED_APPS = (
    # This has to be before django.contrib.admin
    # 'grappelli',  # http://django-grappelli.readthedocs.org/en/latest/quickstart.html#installation

    # Core Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third party apps
    'crispy_forms',  # http://django-crispy-forms.readthedocs.org/en/latest/
    'braces',  # http://django-braces.readthedocs.org/en/v1.4.0/
    'post_office',

    # Custom apps
    'accounts',
    'apps.keywords',
    'apps.meetup',
    'apps.websites',
    'apps.content',
    'apps.twitter',
    'apps.affiliates',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'oxidizr.urls'

WSGI_APPLICATION = 'oxidizr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oxidizr',
        'USER': 'postgres',
        'HOST': '127.0.0.1'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/var/www/example.com/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected', 'static')

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets', 'static'),
)

AUTH_USER_MODEL = 'accounts.User'

DATE_FORMAT_PYTHON = '%d/%m/%Y'
DATE_FORMAT_JS = 'DD/MM/YYYY'
DATE_FORMAT_TEMPLATE = 'j/m/Y'

TIME_FORMAT_PYTHON = '%I:%M %p'
TIME_FORMAT_JS = ''
TIME_FORMAT_TEMPLATE = 'h:i A'

DATETIME_FORMAT_TEMPLATE = '%s %s' % (DATE_FORMAT_TEMPLATE, TIME_FORMAT_TEMPLATE)
DATETIME_FORMAT_PYTHON = '%s %s' % (DATE_FORMAT_PYTHON, TIME_FORMAT_PYTHON)

# Enable Django to parse date and time in our needed formats
DATE_INPUT_FORMATS = [DATE_FORMAT_PYTHON]
TIME_INPUT_FORMATS = [TIME_FORMAT_PYTHON]

# Enable Django to print date and time in our needed formats
DATE_FORMAT = DATE_FORMAT_TEMPLATE
TIME_FORMAT = TIME_FORMAT_TEMPLATE
DATETIME_FORMAT = '%s %s' % (DATE_FORMAT_TEMPLATE, TIME_FORMAT_TEMPLATE)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SITE_ID = 1

DEFAULT_FROM_EMAIL = 'Oxidizr <hello@oxidizr.com>'

try:
    from local_settings import *
except ImportError:
    pass