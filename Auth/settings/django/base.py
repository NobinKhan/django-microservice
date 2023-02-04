# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
from os import path
from settings.env import BASE_DIR, env

env.read_env(path.join(BASE_DIR, ".env"))

# Security key, debug and host config
SECRET_KEY = env('DJANGO_SECRET_KEY', default="django-insecure-!5dukt(mra33vv@e4(ls(u-66tjobl!t^m2aidv7$q6ik-lfow")
DEBUG = env.bool("DJANGO_DEBUG", default=True)
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
        'NAME': env('AUTHDB_DB_NAME'),
        'USER': env('AUTHDB_USER'),
        'PASSWORD': env('AUTHDB_PASSWORD'),
        'HOST': env('AUTHDB_HOST'),
        'PORT': env('AUTHDB_PORT'),
    },
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True

if env("GITHUB_WORKFLOW"):
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
        "BACKEND": env('REDIS_BACKEND'),
        "LOCATION": env('REDIS_LOCATION'),
    }
}
SESSION_ENGINE = env('SESSION_ENGINE')
SESSION_CACHE_ALIAS = env('SESSION_CACHE_ALIAS')


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
APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")


# Custom Auth Config
AUTH_USER_MODEL = 'account.User'


# Internationalization
USE_TZ = True
USE_I18N = True
USE_L10N = True
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"


# media files config
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Import Other Settings
from settings.others.drf import *
from settings.others.celery import *  # noqa
from settings.others.cors import *  # noqa
from settings.others.files_and_storages import *  # noqa
from settings.others.pyseto import *  # noqa
from settings.others.sentry import *  # noqa
from settings.others.sessions import *  # noqa

from settings.others.debug_toolbar.settings import *  # noqa
from settings.others.debug_toolbar.setup import DebugToolbarSetup  # noqa

INSTALLED_APPS, MIDDLEWARE = DebugToolbarSetup.do_settings(INSTALLED_APPS, MIDDLEWARE)