"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tJqV5fYo3crpL1+JI2kcCyTOACp81WFWRNQ2r8dET8M='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # os.environ.get('DEBUG', False)
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'auto-key',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'mirage',
    'corsheaders',
    'main',
    'user',
    'document',
    'connection',
    'jobs',
    'django_apscheduler',
    'channels',
    'mptt'
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend', 'dist')],
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
WSGI_APPLICATION = 'main.wsgi.application'
ASGI_APPLICATION = 'main.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

CONN_MAX_AGE = 300
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': os.environ.get('DB_LOCATION', 'localhost'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend', 'dist', 'static'),
)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'frontend', 'dist', 'static'),
    )
else:
    # STATIC_ROOT = os.path.join(BASE_DIR, 'main', "frontend", "dist", "static")
    # STATIC_ROOT = os.path.join(BASE_DIR, 'main', "frontend", "dist", "static")
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

AUTH_USER_MODEL = 'user.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

redis_key = os.environ.get('BROKER_KEY', 'redis')
redis_host = os.environ.get('BROKER_HOST', '127.0.0.1')
redis_url = 'redis://:' + redis_key + '@' + redis_host + ':6379'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [redis_url],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'main'
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [redis_url],
            'channel_capacity': {
                'daphne.response*': 10000,  # Important for stability
                'http.connect': 1000,
                'http.request': 1000,
                'http.response*': 1000,
                'http.disconnect': 1000,
                'websocket.receive': 1000,
                'websocket.send*': 1000,
                'websocket.connect': 2000,
                'websocket.disconnect': 1000,
            },
            # "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'DEBUG',
            },
            'asyncio': {
                'level': 'WARNING',
            },
            'daphne': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'DEBUG'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }

PROJECT_DOCUMENTS_PATH = 'project_documents'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_DEFAULT_USER = 'turkaybiliyor@hotmail.com'
