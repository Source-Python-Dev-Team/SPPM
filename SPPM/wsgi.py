"""
WSGI config for SPPM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import os

# Django
from django.core.wsgi import get_wsgi_application


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPPM.settings")

application = get_wsgi_application()
