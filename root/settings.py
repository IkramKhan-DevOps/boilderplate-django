import datetime
from pathlib import Path
import environ

""" APPLICATION CONFIGURATIONS """

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, True)
)
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = True
SECRET_KEY = env('SECRET_KEY')
ENVIRONMENT = env('ENVIRONMENT')
SITE_ID = int(env('SITE_ID'))

DOMAIN = env('DOMAIN')
PROTOCOL = env('PROTOCOL')
BASE_URL = f"{PROTOCOL}://{DOMAIN}"
ALLOWED_HOSTS = str(env('ALLOWED_HOSTS')).split(',')
CSRF_TRUSTED_ORIGINS = [f'{PROTOCOL}://{host}' for host in ALLOWED_HOSTS]
LOGOUT_REDIRECT_URL = '/accounts/cross-auth/'
LOGIN_REDIRECT_URL = '/accounts/cross-auth/'
GOOGLE_CALLBACK_ADDRESS = f"{BASE_URL}/accounts/google/login/callback/"
APPLE_CALLBACK_ADDRESS = f"{BASE_URL}/accounts/apple/login/callback/"

ROOT_URLCONF = 'root.urls'
AUTH_USER_MODEL = 'users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

INSTALLED_APPS = [
    # DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # STARTER APPS
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'phonenumber_field',

    # WEB APPS
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.mfa',

    # REST APPS
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'drf_yasg',

    # YOUR APPS
    'src.core.apps.CoreConfig',
    'src.services.users.apps.UsersConfig',
    'src.services.fee',

    # WEB APPS
    'src.web.website',
    'src.web.accounts',
    'src.web.admins',

    # mailchimp
    'mailchimp_transactional',
    #  'notifications',
]
# MAILCHIMP SETTINGS
MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY')
MAILCHIMP_FROM_EMAIL = env('MAILCHIMP_FROM_EMAIL')
EMAIL_HOST = "smtp.mandrillapp.com"

# GOOGLE SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = "587"
EMAIL_HOST = "smtp.gmail.com"
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

MIDDLEWARE = [
    # DJANGO MIDDLEWARES
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',

    # YOUR MIDDLEWARES
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = (
    # DJANGO BACKENDS
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # YOUR BACKENDS
)

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
                'src.core.context_processors.application'
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

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
EMAIL_BACKEND = 'django.root.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

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
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

""" DEBUGGING TOOLS """

# Make sure to remove this in live server - use it on local server
if ENVIRONMENT != 'server':
    INSTALLED_APPS += [
        'django_browser_reload'
    ]
    MIDDLEWARE += [
        'django_browser_reload.middleware.BrowserReloadMiddleware'
    ]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'CLIENT_ID': '1021579594890-6m3kiukcsku6j5lpcv0293sjc3qq4830.apps.googleusercontent.com',
        'SECRET': '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',
        'SCOPE': ['profile', 'email', 'openid'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

""" MFA SETUP --------------------------------------------------------------------------------"""
MFA_ADAPTER = "allauth.mfa.adapter.DefaultMFAAdapter"

""" GMAIL SMTP ---------------------------------------------------------------------------------"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SMTP  configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = 'gwtw.mhn@gmail.com'
EMAIL_HOST_PASSWORD = 'jyrq jbmd grlu vvzs'

# Default from email address
DEFAULT_FROM_EMAIL = 'exarth@info.com'  # Replace with the email address to appear in the 'from' field

"""  ACCOUNT ADAPTER Modify Login/Signup Redirect UR----------------------------------------------------"""
ACCOUNT_ADAPTER = "src.web.accounts.adapters.MyAccountAdapter"
