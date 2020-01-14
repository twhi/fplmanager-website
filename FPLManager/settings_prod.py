"""
PROD ENVIRONMENT SETTINGS
"""

from .settings_common import *  # IMPORT COMMON SETTINGS

ALLOWED_HOSTS = ['fplmanager.herokuapp.com'] # ['arcane-anchorage-15049.herokuapp.com']  # prod

# AWS S3 bucket credentials
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_BUCKET_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_BUCKET_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_BUCKET_SECRET_ACCESS_KEY') 

# AWS S3 bucket settings
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# Production Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PROD_DB_NAME'),
        'USER': os.environ.get('PROD_DB_USER'),
        'PASSWORD': os.environ.get('PROD_DB_PASSWORD'),
        'HOST': os.environ.get('PROD_DB_HOST'),
        'PORT': 5432,
    }
}

##########################################################################
# # security tips from https://reversepython.net/lab/django-web-security-checklist-deployment/
SECURE_HSTS_SECONDS = 18768000  # ~6 months
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True #to avoid transmitting the CSRF cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True #to avoid transmitting the session cookie over HTTP accidentally.

X_FRAME_OPTIONS = 'DENY'