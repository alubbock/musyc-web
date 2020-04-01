"""
Django settings for musycdjango project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
try:
    import debug_toolbar
except ImportError:
    debug_toolbar = None

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables for .env file, if present
env_file = os.path.join(BASE_DIR, 'musyc.env')
try:
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            var_name, var_val = line.split('=', 1)
            # print('Setting {} from musyc.env'.format(var_name))
            os.environ[var_name] = var_val
except FileNotFoundError:
    pass


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DJANGO_DEBUG'].lower() == 'true'
USE_TLS = os.environ.get('DJANGO_USE_TLS', 'false').lower() == 'true'
if not DEBUG and USE_TLS:
    SESSION_COOKIE_SECURE = True
    CRSF_COOKIE_SECURE = True

HOSTNAME = os.environ.get('DJANGO_HOSTNAME', 'localhost')
ALLOWED_HOSTS = [HOSTNAME, ]
INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'musycweb',
    'custom_user',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'django_celery_results'
]
if DEBUG and debug_toolbar:
    INSTALLED_APPS += ['debug_toolbar']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG and debug_toolbar:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ROOT_URLCONF = 'musycdjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

EMAIL_USE_TLS = True
EMAIL_ENABLED = True
try:
    EMAIL_HOST = os.environ['DJANGO_EMAIL_HOST']
    EMAIL_PORT = os.environ['DJANGO_EMAIL_PORT']
    EMAIL_HOST_USER = os.environ['DJANGO_EMAIL_USER']
    EMAIL_HOST_PASSWORD = os.environ['DJANGO_EMAIL_PASSWORD']
    DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_EMAIL_FROM', EMAIL_HOST_USER)
except KeyError:
    if DEBUG:
        EMAIL_ENABLED = False
    else:
        raise

AUTH_USER_MODEL = 'custom_user.EmailUser'
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none' if DEBUG else 'mandatory'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_FORMS = {'login': 'musycweb.forms.CentredAuthForm',
                 'change_password': 'musycweb.forms.ChangePasswordForm',
                 'reset_password': 'musycweb.forms.ResetPasswordForm',
                 'reset_password_from_key': 'musycweb.forms.ResetPasswordKeyForm',
                 'set_password': 'musycweb.forms.SetPasswordForm',
                 'signup': 'musycweb.forms.SignUpForm',
                 'add_email': 'musycweb.forms.AddEmailForm'}
LOGIN_REDIRECT_URL = 'index'

WSGI_APPLICATION = 'musycdjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASE_SETTING = os.environ.get('DJANGO_DATABASE', 'postgres')
if DATABASE_SETTING == 'postgres':
    # Bigger batch size is faster but uses more memory
    DB_MAX_BATCH_SIZE = 100000
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'NAME': os.environ.get('POSTGRES_DB', False) or
                    os.environ.get('POSTGRES_USER', 'postgres'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'PORT': os.environ.get('POSTGRES_PORT', '')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True
DATETIME_FORMAT = 'Y-m-d H:i:s e'

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
if 'DJANGO_STATIC_ROOT' in os.environ:
    STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Celery
CELERY_RESULT_BACKEND = 'django-db'
RABBITMQ_USER = os.environ.get('RABBITMQ_DEFAULT_USER', 'guest')
RABBITMQ_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL',
    f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}//'
)
from kombu import Queue, Exchange
CELERY_TASK_DEFAULT_PRIORITY = 5
CELERY_TASK_QUEUE_MAX_PRIORITY = 10
CELERY_TASK_QUEUES = (
    Queue('celery', Exchange('celery'),
          routing_key='celery',
          queue_arguments={'x-max-priority': CELERY_TASK_QUEUE_MAX_PRIORITY}),
)
# Time limit before tasks are aborted (24 hours)
CELERY_TASK_SOFT_TIME_LIMIT = 60 * 60 * 24
# Datasets with more tasks than this are run at priority=3
CELERY_DEPRIORITISE_SIZE_L3 = 1000
# Datasets with more tasks than this are run at priority=2
CELERY_DEPRIORITISE_SIZE_L2 = 10000

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

if not DEBUG and 'SENTRY_DSN' in os.environ:
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration(), CeleryIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
