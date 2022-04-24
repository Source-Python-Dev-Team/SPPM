"""Inline for Plugin admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectImageInline,
    ProjectTagInline,
)
from project_manager.plugins.models import (
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginTag,
    SubPluginPath,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginContributorInline',
    'PluginGameInline',
    'PluginImageInline',
    'PluginTagInline',
    'SubPluginPathInline',
)


# =============================================================================
# INLINES
# =============================================================================
class PluginContributorInline(ProjectContributorInline):
    """Plugin Contributor Admin Inline."""

    model = PluginContributor


class PluginGameInline(ProjectGameInline):
    """Plugin Game Admin Inline."""

    model = PluginGame


class PluginTagInline(ProjectTagInline):
    """Plugin Tag Admin Inline."""

    model = PluginTag


class PluginImageInline(ProjectImageInline):
    """Plugin Image Inline."""

    model = PluginImage


class SubPluginPathInline(admin.StackedInline):
    """SubPluginPath Inline."""

    extra = 0
    view_on_site = False
    fields = (
        'path',
        'allow_module',
        'allow_package_using_basename',
        'allow_package_using_init',
    )
    model = SubPluginPath

    def has_add_permission(self, request, obj=None):
        """Disallow adding new images in the Admin."""
        return False
