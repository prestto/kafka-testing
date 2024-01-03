from pathlib import Path

from kombu import Exchange, Queue

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%3ef(wo*@e6)vjzvqh37hw7x6b5&bvm42(z5(xu!wamjrd!x_)"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app_core.interface.urls"

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

# WSGI_APPLICATION = 'django_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery Configuration
CELERY_BROKER_URL = "amqp://rabbit_user:rabbit_password@rabbitmq-service:5672"
CELERY_ENABLED = True

CELERY_TIMEZONE = "UTC"

# By default all tasks will go to default.
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default_exchange"
CELERY_DEFAULT_ROUTING_KEY = "default_queue"

# Exchange for peripheral app.
PERIPHERAL_EXCHANGE = "peripheral_exchange"
peripheral_exchange = Exchange(name=PERIPHERAL_EXCHANGE, type="topic")

# Crossover queues.
PERIPHERAL_QUEUE_ONE = "peripheral_queue.one"
PERIPHERAL_QUEUE_TWO = "peripheral_queue.two"
PERIPHERAL_QUEUE_THREE = "peripheral_queue.three"

# Message routing: https://docs.celeryq.dev/en/stable/userguide/configuration.html#message-routing
# Basics: https://docs.celeryq.dev/en/stable/userguide/routing.html#automatic-routing
# Routes: https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-routes
CELERY_QUEUES = [
    Queue(
        name=CELERY_DEFAULT_QUEUE,
        exchange=CELERY_DEFAULT_EXCHANGE,
        routing_key=CELERY_DEFAULT_ROUTING_KEY,
    ),
    Queue(
        name=PERIPHERAL_QUEUE_ONE,
        exchange=peripheral_exchange,
        routing_key="app_peripheral.yes",
    ),
    Queue(
        name=PERIPHERAL_QUEUE_TWO,
        exchange=peripheral_exchange,
        routing_key="app_peripheral.yes",
    ),
    Queue(
        name=PERIPHERAL_QUEUE_THREE,
        exchange=peripheral_exchange,
        routing_key="app_peripheral.no",
    ),
]

CELERY_ROUTES = {
    "app_peripheral.interface.tasks.*:": {"exchange": "peripheral_exchange"},
}
