from .base import *

DEBUG = True
LOCAL = True

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
TEMPLATES[0]['DIRS'].append(BASE_DIR / 'local-templates')
LOGIN_REDIRECT_URL = '/'
