"""
WSGI config for plugin_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
import os

# Django Imports
from django.core.wsgi import get_wsgi_application


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plugin_manager.settings")

application = get_wsgi_application()
