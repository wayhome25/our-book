"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

# 비밀파일패턴 적용을 위한 메소드
def get_secret(settings):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[settings]
    except KeyError:
        error_msg = "Set the {} environment variable".format(settings)
        raise ImproperlyConfigured(error_msg)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# naver api 설정
CLIENT_ID = get_secret("CLIENT_ID")
CLIENT_SECRET = get_secret("CLIENT_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'debug_toolbar',
    'django_extensions',
    'django_messages',

    'accounts',
    'books',
]

SITE_ID = 1

# AUTHENTICATION
AUTH_USER_MODEL = 'accounts.MyUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'accounts.context_processors.forms',
                
                'django_messages.context_processors.inbox',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Debug Toolbar Setting
INTERNAL_IPS = ["127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'our_book',
        'USER': 'wayhome25',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '1234',
        'ATOMIC_REQUESTS' : True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static') # A list of locations of additional static files
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email

EMAIL_PASSWORD = get_secret("EMAIL_PASSWORD")

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wayhome250@gmail.com'
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://localhost:6379/'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/'

# SLACK SETTINGS
SLACK_TOKEN = get_secret("SLACK_TOKEN")
