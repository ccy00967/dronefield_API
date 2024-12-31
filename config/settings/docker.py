from .base import *

ALLOWED_HOSTS = ["*"]

DEBUG = True
#DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}

CORS_ORIGIN_WHITELIST += [
    "https://dronefield.co.kr",
    "https://dronefield.co.kr:8080",
]

CORS_ALLOWED_ORIGINS += [ 
    "https://dronefield.co.kr",
    "https://dronefield.co.kr:8080",
]

CSRF_TRUSTED_ORIGINS += [
    "https://dronefield.co.kr",
    "https://dronefield.co.kr:8080",
]