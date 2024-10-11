from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wufto_balances', #wufto_balances
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
STATICFILES_DIRS = (BASE_DIR, 'static')