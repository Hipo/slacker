from slacker.settings.base import *  # noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = secrets.SECRET_KEY

DEBUG = False

SERVER_URL = "http://slacker.hack.hipolabs.com"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'slacker.hack.hipolabs.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': "slacker",
        'USER': "slacker",
        'PASSWORD': secrets.POSTGRES_PASSWORD,
        'HOST': "hackdb.cmq91upkqjfq.us-east-1.rds.amazonaws.com",
        'PORT': '5432',
    }
}

sentry_sdk.init(
    dsn=secrets.SENTRY_DSN,
    integrations=[DjangoIntegration()]
)
