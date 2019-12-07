"""
DEV ENVIRONMENT SETTINGS
"""
import os
from .settings_common import *  # IMPORT COMMON SETTINGS

DEBUG = True

ALLOWED_HOSTS = []

# Dev database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('FPL_DEV_DB_NAME'),
        'USER': os.environ.get('FPL_DEV_DB_USER'),
        'PASSWORD': os.environ.get('FPL_DEV_DB_PASSWORD'),
        'HOST': os.environ.get('FPL_DEV_DB_HOST'),
        'PORT': os.environ.get('FPL_DEV_DB_PORT'),
    }
}