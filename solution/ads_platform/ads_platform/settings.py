from os import getenv
from pathlib import Path

from django_s3_storage.storage import S3Storage
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


def load_bool_value(key: str) -> bool:
    value = getenv(key, "0")
    return value in ["1", "yes", "YES", "True", "true", "y", "Y", "T", "t"]


DO_NOT_LOAD_FROM_ENV = load_bool_value("RUNNED_IN_DOCKER")
if not DO_NOT_LOAD_FROM_ENV:
    load_dotenv()

# base settings
SECRET_KEY = getenv("DJANGO_SECRET_KEY", "АЛЕКСАНДР ШАХОВ Я ВАШ ФАНАТ")
DEBUG = load_bool_value("DJANGO_DEBUG")
ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
MODERATION_ENABLED = False

# yagpt creds
YAGPT_FOLDER_ID = getenv("YAGPT_FOLDER_ID", "0")
YAGPT_AUTH = getenv("YAGPT_AUTH", "0")

# yagpt base prompts
MODERATION_START_PROMPT = """Представь себе, что ты модератор сервиса Яндекс Директ, и тебе нужно модерировать текст рекламных объявлений. 
Тебе нужно отвечать ДА ИЛИ НЕТ, другие ответы не допускаются.

Если ты отвечаешь НЕТ, то на новой строке пиши ТОЛЬКО ПРИЧИНУ, почему ты отклоняешь объявление

Если ты сомневаешься в своем выборе, то скажи НЕ ЗНАЮ"""  # noqa


# s3 storage setup
AWS_REGION = "ru-central1"
AWS_ACCESS_KEY_ID = getenv("S3_ID")
AWS_SECRET_ACCESS_KEY = getenv("S3_SECRET")
AWS_S3_ENDPOINT_URL = "https://storage.yandexcloud.net"
AWS_BUCKET_NAME = "taprod"
AWS_S3_BUCKET_AUTH = False
AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365

S3 = S3Storage(aws_s3_bucket_name=AWS_BUCKET_NAME)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_s3_storage",
    # my applications
    "clients.apps.ClientsConfig",
    "advertisers.apps.AdvertisersConfig",
    "mlscores.apps.MlscoresConfig",
    "campaigns.apps.CampaignsConfig",
    "ads.apps.AdsConfig",
    "internal.apps.InternalConfig",
    "stats.apps.StatsConfig",
    "config.apps.ConfigConfig"
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

ROOT_URLCONF = "ads_platform.urls"

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

WSGI_APPLICATION = "ads_platform.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DATABASE", "postgres"),
        "HOST": getenv("POSTGRES_HOST", "localhost"),
        "PORT": getenv("POSTGRES_PORT", "5432"),
        "USER": getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": getenv("POSTGRES_PASSWORD", "postgres"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib."
            "auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib."
            "auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib."
            "auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib."
            "auth.password_validation.NumericPasswordValidator"
        ),
    },
]

# Timezone settings
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Statis settings
STATIC_URL = "static/"

# Other
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
