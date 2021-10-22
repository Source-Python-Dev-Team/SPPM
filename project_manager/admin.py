"""Base app admin."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Django
from django.contrib import admin
from django.contrib.auth import models

# Third Party Django
from precise_bbcode.models import BBCodeTag, SmileyTag


# =============================================================================
# UNREGISTER
# =============================================================================
admin.site.unregister(models.Group)
admin.site.unregister(BBCodeTag)
admin.site.unregister(SmileyTag)


# =============================================================================
# ADMINS
# =============================================================================
import_module('project_manager.packages.admin')
import_module('project_manager.plugins.admin')
import_module('project_manager.sub_plugins.admin')
