"""SubPlugin admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
import copy

# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin
from project_manager.sub_plugins.admin.inlines import (
    SubPluginContributorInline,
    SubPluginGameInline,
    SubPluginImageInline,
    SubPluginReleaseInline,
    SubPluginTagInline,
)
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAdmin',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
_project_fieldsets = copy.deepcopy(ProjectAdmin.fieldsets)
_fields = _project_fieldsets[0][1]['fields']
_project_fieldsets[0][1]['fields'] = ('plugin',) + _fields


# =============================================================================
# ADMINS
# =============================================================================
@admin.register(SubPlugin)
class SubPluginAdmin(ProjectAdmin):
    """SubPlugin admin."""

    fieldsets = _project_fieldsets
    inlines = (
        SubPluginContributorInline,
        SubPluginGameInline,
        SubPluginImageInline,
        SubPluginTagInline,
        SubPluginReleaseInline,
    )
    list_display = ProjectAdmin.list_display + (
        'plugin',
    )
    readonly_fields = ProjectAdmin.readonly_fields + (
        'plugin',
    )
    search_fields = ProjectAdmin.search_fields + (
        'plugin__name',
        'plugin__basename',
    )
