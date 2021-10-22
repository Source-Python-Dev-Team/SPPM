"""Inline for Plugin admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectImageInline,
    ProjectReleaseInline,
    ProjectTagInline,
)
from project_manager.plugins.models import (
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
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
    'PluginReleaseInline',
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


class PluginReleaseInline(ProjectReleaseInline):
    """Plugin Release Inline."""

    model = PluginRelease


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
    readonly_fields = (
        'path',
    )
    model = SubPluginPath

    def has_add_permission(self, request, obj):
        """Disallow adding new images in the Admin."""
        return False
