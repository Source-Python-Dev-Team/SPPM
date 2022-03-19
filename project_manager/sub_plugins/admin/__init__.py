"""SubPlugin admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from copy import deepcopy

# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin, ProjectReleaseAdmin
from project_manager.sub_plugins.admin.inlines import (
    SubPluginContributorInline,
    SubPluginGameInline,
    SubPluginImageInline,
    SubPluginTagInline,
)
from project_manager.sub_plugins.models import SubPlugin, SubPluginRelease


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAdmin',
    'SubPluginReleaseAdmin',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
_project_fieldsets = deepcopy(ProjectAdmin.fieldsets)
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


@admin.register(SubPluginRelease)
class SubPluginReleaseAdmin(ProjectReleaseAdmin):
    """SubPluginRelease admin."""

    fieldsets = deepcopy(ProjectReleaseAdmin.fieldsets)
    fieldsets[0][1]['fields'] += ('sub_plugin',)
    list_display = ProjectReleaseAdmin.list_display + ('sub_plugin',)
    ordering = ('sub_plugin', '-created',)
    readonly_fields = ProjectReleaseAdmin.readonly_fields + ('sub_plugin',)
    search_fields = ProjectReleaseAdmin.search_fields + ('sub_plugin__name',)
