"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
from pathlib import Path

import datetime as datetime
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, True)
)
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = True
SERVER = False
AUTH_USER_MODEL = 'accounts.User'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/cross-auth/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY = env('SECRET_KEY')
ENVIRONMENT = env('ENVIRONMENT')
ALLOWED_HOSTS = [env('ALLOWED_HOST')]
GOOGLE_CALLBACK_ADDRESS = env('GOOGLE_CALLBACK_URL')
SITE_ID = int(env('SITE_ID'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # REQUIRED_APPLICATIONS
    'crispy_forms',
    'ckeditor',
    'django_filters',
    'phonenumber_field',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework_swagger',

    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',

    'src.api.apps.ApiConfig',
    'src.website.apps.WebsiteConfig',
    'src.accounts.apps.AccountsConfig',
    'src.administration.admins.apps.AdministrationAdminConfig'
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

if ENVIRONMENT == 'server':
    DATABASES = {
        'default': {
            'ENGINE': env('DB_ENGINE'),
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASS'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

""" INTERNATIONALIZATION --------------------------------------------------------------------------------"""
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" EMAIL CONFIGURATION --------------------------------------------------------------------------------"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
DEFAULT_FROM_EMAIL = "noreply@thestaffmanager.com"

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'assets'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'JPEG': ".jpg",
    'PNG': ".png",
    'GIF': ".gif"
}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

""" ALL-AUTH SETUP --------------------------------------------------------------------------------"""

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

"""


TEST DATA FOR >ENV
------------------------------------------------
ENVIRONMENT=local
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_HOST=localhost
DB_USER=thestaffmanagerdbrootuser
DB_PASS=thestaffmanagerdbrootuserpassword
DB_NAME=thestaffmanagerdb
DB_PORT=django.db.backends.postgresql_psycopg2
EMAIL_USE_TLS=True
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=donald.duck0762@gmail.com
EMAIL_HOST_PASSWORD=iblqezaitfuxxbfg
EMAIL_PORT=587
BASE_URL=http://127.0.0.1:8000
DEFAULT_FROM_EMAIL=Support-Team <mark@exarth.com>
DEBUG=True
SECRET_KEY=YUwsjlxk30PYf6dovmiUK8c0i1MARKIiejYh7kSDv3fiBq2mlWmeXap
TIME_ZONE=Asia/Karachi
GOOGLE_CALLBACK_URL=http://127.0.0.1:8000/accounts/google/login/callback/
ALLOWED_HOST=127.0.0.1
SITE_ID=1
"""
