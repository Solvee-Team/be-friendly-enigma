import os
from pathlib import Path
from firebase_admin import initialize_app


SECRET_KEY = 'django-insecure-b3y%-yh&dq9f=0zc@_fg8a-kvksm(*p8qr=uu9^4wvhv!q-3^('

DEBUG = True

ALLOWED_HOSTS = ["*"]

BASE_DIR = Path(__file__).resolve().parent.parent
FIREBASE_APP = initialize_app()
CHANNEL_LAYER_CLASS = os.environ.get(
    "CHANNEL_LAYER", "channels_rabbitmq.core.RabbitmqChannelLayer"
)

REDIS_CONFIG = {
    "hosts": [
        os.environ.get("REDIS_HOST", "redis://:redis_pass@friendly_enigma_redis:6379/0")
    ],
}
RMQ_CONFIG = {"host": os.environ.get("RMQ_HOST", "amqp://guest:guest@127.0.0.1:5672/")}

CHANNEL_LAYER_CONFIG = (
    REDIS_CONFIG
    if CHANNEL_LAYER_CLASS == "channels_redis.core.RedisChannelLayer"
    else RMQ_CONFIG
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "user",
    "chat",
    "notifications",
    "corsheaders",
    "fcm_django",
    "django_celery_beat",
    "channels",
    "rest_framework_simplejwt",
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "request_logging.middleware.LoggingMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'friendly_enigma.urls'
AUTH_USER_MODEL = "user.User"


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

WSGI_APPLICATION = 'friendly_enigma.wsgi.application'
ASGI_APPLICATION = 'friendly_enigma.routing.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

CORS_ALLOW_ALL_ORIGINS = True

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": CHANNEL_LAYER_CLASS,
        "CONFIG": CHANNEL_LAYER_CONFIG,
    },
}

SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    # todo change in non local env to RSA private key
    "SIGNING_KEY": SECRET_KEY,
    "UPDATE_LAST_LOGIN": True,
}

CELERY_BROKER_URL = os.environ.get("RMQ_HOST", "amqp://guest:guest@127.0.0.1:5672/")
CELERY_RESULT_BACKEND = "cache+memcached://127.0.0.1:11211/"
