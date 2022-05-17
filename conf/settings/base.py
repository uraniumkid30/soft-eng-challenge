import os
import functools
from pathlib import Path
from conf.addons.directories import *  # noqa
from conf.addons.logs import get_logs_settings

INTERNAL_IPS = ("127.0.0.1",)

LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"

ANONYMOUS_URLS = [
    r"^admin/$",
    r"^admin/login/$",
    r"^media/",
    r"^static/",
]

# Application definition

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
LOCAL_APPS = [
    "applications.ship",
    "applications.account",
    "applications.configuration",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_jwt",
    "graphene_django",
    "django_object_actions",
    "drf_spectacular",
    "django_extensions",
    # "whitenoise.runserver_nostatic",
]

ALL_APPS_CONTAINER = {
    "DEFAULT_APPS": DEFAULT_APPS,
    "LOCAL_APPS": LOCAL_APPS,
    "THIRD_PARTY_APPS": THIRD_PARTY_APPS,
}

# Application definition
INSTALLED_APPS: list = functools.reduce(lambda x, y: x + y, ALL_APPS_CONTAINER.values())


ALLOWED_HOSTS = []


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(THEME_DIR, "templates")],
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

WSGI_APPLICATION = "conf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "/var/www/personal_projects/TodoApp/static"  # is the folder location of static files when collectstatic is run

MEDIA_URL = "media/"
MEDIA_ROOT = "/var/www/personal_projects/TodoApp/media"

STATICFILES_DIRS = [
    os.path.join(THEME_DIR, "static"),
]  # tells Django where to look for static files in a Django project, such as a top-level static folder

# DJANGO_STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
# WHITENOISE_STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.User"
swappable = "AUTH_USER_MODEL"
LOGGING = get_logs_settings(LOGS_DIR)
PROJECT_NAME = "MotherShip"

from conf.addons.cors import *  # noqa
from conf.addons.jwt import *  # noqa
from conf.addons.sessions import *  # noqa
from conf.addons.celery import *  # noqa
from conf.addons.rest_frame_work import *  # noqa
from conf.addons.constants import *  # noqa
