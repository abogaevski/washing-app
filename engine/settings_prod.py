"""
Django settings for engine project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.contrib.messages import constants as messages


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1@%%-0%_9sb$1474f7_&n4&xy3ta5tpocrusx6ng(8$g$t(8yr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'engine.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.contractor_list',
                'app.context_processors.station_list'
            ],
        },
    },
]

WSGI_APPLICATION = 'engine.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'djangouser',
        'PASSWORD': 'xdsI_Abah%wash',
        'CONN_MAX_AGE': 3600
    }
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mqtt_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/mqtt_debug.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'verbose'
        },
        'django_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 7,
            'formatter': 'verbose'
        },
        'tasks_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/tasks.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 7,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'mqtt': {
            'level': 'DEBUG',
            'handlers': ['mqtt_file'],
            'propagate': True,
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['django_file'],
            'propagate': True,
        },
        'tasks': {
            'level': 'DEBUG',
            'handlers': ['tasks_file'],
            'propagate': True,
        }
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
}

# REDIS related settings 
CELERY_REDIS_HOST = 'localhost'
CELERY_REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + CELERY_REDIS_HOST + ':' + CELERY_REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
CELERY_CELERY_RESULT_BACKEND = 'redis://' + CELERY_REDIS_HOST + ':' + CELERY_REDIS_PORT + '/0'

CELERY_BEAT_SCHEDULE = {
    'check_post_availability': {
        'task': 'app.tasks.check_post_availability',
        'schedule': 60.0,
    }
}

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'notify.by.carwash@yandex.by'
EMAIL_HOST_PASSWORD = '8y#c4rW45h'
EMAIL_PORT = 587
EMAIL_USE_TLS = True