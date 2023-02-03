# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

from os import environ
from settings.env import BASE_DIR


# Security key, debug and host config
SECRET_KEY = environ.get('DJANGO_SECRET_KEY')
DEBUG = True if environ.get('DEBUG', default='False') == 'True' else False
ALLOWED_HOSTS = ["*"]


# Application definition
FIRST_PRIORITY_APPS = [

]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_jwt",

    'django_countries',
    "phonenumber_field",

    # "django_celery_results",
    # "django_celery_beat",
    # "django_filters",
    # "django_extensions",
]

LOCAL_APPS = [
    "apps.user.apps.UserConfig",
]

INSTALLED_APPS = [
    *FIRST_PRIORITY_APPS,
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]


# Middleware config
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware", # Cors headers middleware
    "whitenoise.middleware.WhiteNoiseMiddleware", #whitenoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Template Configs
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Database Configs
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('AUTH_DB'),
        'USER': environ.get('AUTH_USER'),
        'PASSWORD': environ.get('AUTH_PASSWORD'),
        'HOST': environ.get('AUTH_HOST'),
        'PORT': environ.get('AUTH_PORT'),
    },
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True

if environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }


# redis cache
CACHE_TTL = 60 * 1500
CACHES = {
    "default": {
        "BACKEND": environ.get('REDIS_BACKEND'),
        "LOCATION": environ.get('REDIS_LOCATION'),
    }
}
SESSION_ENGINE = environ.get('SESSION_ENGINE')
SESSION_CACHE_ALIAS = environ.get('SESSION_CACHE_ALIAS')


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Project wide configs
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "settings.wsgi.application"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom Auth Config
AUTH_USER_MODEL = 'account.User'


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# media files config
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/webfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "styleguide_example.api.exception_handlers.drf_default_with_modifications_exception_handler",
    # 'EXCEPTION_HANDLER': 'styleguide_example.api.exception_handlers.hacksoft_proposed_exception_handler',
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": [],
}

APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")


from config.settings.celery import *  # noqa
from config.settings.cors import *  # noqa
from config.settings.email_sending import *  # noqa
from config.settings.files_and_storages import *  # noqa
from config.settings.jwt import *  # noqa
from config.settings.sentry import *  # noqa
from config.settings.sessions import *  # noqa