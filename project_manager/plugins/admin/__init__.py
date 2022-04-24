"""Plugin admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from copy import deepcopy

# Django
from django.contrib import admin

# App
from project_manager.admin.base import ProjectAdmin, ProjectReleaseAdmin
from project_manager.plugins.admin.inlines import (
    PluginContributorInline,
    PluginGameInline,
    PluginImageInline,
    PluginTagInline,
    SubPluginPathInline,
)
from project_manager.plugins.models import Plugin, PluginRelease


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAdmin',
    'PluginReleaseAdmin',
)


# =============================================================================
# ADMINS
# =============================================================================
@admin.register(Plugin)
class PluginAdmin(ProjectAdmin):
    """Plugin admin."""

    inlines = (
        PluginContributorInline,
        PluginGameInline,
        PluginImageInline,
        PluginTagInline,
        SubPluginPathInline,
    )


@admin.register(PluginRelease)
class PluginReleaseAdmin(ProjectReleaseAdmin):
    """PluginRelease admin."""

    fieldsets = deepcopy(ProjectReleaseAdmin.fieldsets)
    fieldsets[0][1]['fields'] += ('plugin',)
    list_display = ProjectReleaseAdmin.list_display + ('plugin',)
    ordering = ('plugin', '-created',)
    readonly_fields = ProjectReleaseAdmin.readonly_fields + ('plugin',)
    search_fields = ProjectReleaseAdmin.search_fields + ('plugin__name',)

    def get_queryset(self, request):
        """Cache 'plugin' for the queryset."""
        return super().get_queryset(
            request=request,
        ).select_related(
            'plugin',
        )
