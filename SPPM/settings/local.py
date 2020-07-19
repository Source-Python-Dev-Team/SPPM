from .base import *

DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django.template.context_processors.debug',
]
