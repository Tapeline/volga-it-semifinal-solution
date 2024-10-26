"""
Django settings for hospital_service project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import logging
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY") or 'django-insecure-w!mt#31di^7v22vrn-i-(v#%7umz$hg%2szz0f&y3band0k8_9'
MODE = os.getenv("MODE") or "local"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = MODE == "local"


ALLOWED_HOSTS = []
if "ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    "rest_framework",
    "api",
    "drf_yasg"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "api.middleware.SyncCorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hospital_service.urls'

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

WSGI_APPLICATION = 'hospital_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "local": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "hospital_db",
        "USER": os.environ.get("PG_USER") or "pguser",
        "PASSWORD": os.environ.get("PG_PASS") or "pgpass",
        "HOST": "localhost",
        "PORT": "5701",
    },
    "production": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "hospital_db",
        "USER": os.environ.get("PG_USER"),
        "PASSWORD": os.environ.get("PG_PASS"),
        "HOST": os.environ.get("PG_HOST"),
        "PORT": os.environ.get("PG_PORT"),
    }
}
DATABASES["default"] = DATABASES[MODE]
logging.info(f"Using database {DATABASES[MODE]['USER']}@"
             f"{DATABASES[MODE]['HOST']}/"
             f"{DATABASES[MODE]['NAME']}")


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "api.authentication.RemoteAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    "DEFAULT_PARSER_CLASSES": (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    )
}

CORS_ALLOW_ALL_ORIGINS = True
ACCOUNT_SERVICE = os.getenv("ACCOUNT_SERVICE") or "http://localhost:8081"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "static"
