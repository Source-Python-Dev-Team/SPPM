"""Plugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin
from project_manager.plugins.admin.inlines import (
    PluginContributorInline,
    PluginGameInline,
    PluginTagInline,
)
from project_manager.plugins.models import (
    Plugin,
    PluginImage,
    PluginRelease,
    SubPluginPath,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAdmin',
    'PluginImageAdmin',
    'PluginReleaseAdmin',
    'SubPluginPathAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(Plugin)
class PluginAdmin(ProjectAdmin):
    """Plugin admin."""

    inlines = (
        PluginContributorInline,
        PluginGameInline,
        PluginTagInline,
    )


@admin.register(PluginRelease)
class PluginReleaseAdmin(admin.ModelAdmin):
    """PluginRelease admin."""

    list_display = (
        'plugin',
    )
    readonly_fields = (
        'plugin',
    )
    search_fields = (
        'plugin__name',
        'plugin__basename',
        'plugin__owner__user__username',
        'plugin__contributors__user__username',
    )


@admin.register(PluginImage)
class PluginImageAdmin(admin.ModelAdmin):
    """PluginImage admin."""

    list_display = (
        'plugin',
        'image',
    )
    readonly_fields = (
        'plugin',
    )
    search_fields = (
        'plugin__name',
        'plugin__basename',
    )


@admin.register(SubPluginPath)
class SubPluginPathAdmin(admin.ModelAdmin):
    """SubPluginPath admin."""

    actions = None
    list_display = (
        'plugin',
        'path',
    )
    readonly_fields = (
        'path',
        'plugin',
    )
    search_fields = (
        'path',
        'plugin__name',
        'plugin__basename',
    )
    view_on_site = False

    def has_add_permission(self, request):
        """Disallow adding a SubPluginPath in the Admin."""
        return False
