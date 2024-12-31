from .base import *

ALLOWED_HOSTS = ["*"]


DEBUG = True
#DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "df_dj",
        "USER": "chulyoung",
        "PASSWORD": "1234",
        "HOST": DATABASES_HOST,
        "PORT": PORT,
    }
}

