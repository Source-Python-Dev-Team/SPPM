"""Plugin admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin
from project_manager.plugins.admin.inlines import (
    PluginContributorInline,
    PluginGameInline,
    PluginImageInline,
    PluginReleaseInline,
    PluginTagInline,
    SubPluginPathInline,
)
from project_manager.plugins.models import Plugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAdmin',
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
        PluginReleaseInline,
    )
