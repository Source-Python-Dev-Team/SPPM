# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import OldPluginRelease
from .models import Plugin
from .models import PluginImage
from .models import SubPluginPath


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OldPluginReleaseAdmin',
    'PluginAdmin',
    'PluginImageAdmin',
    'SubPluginPathAdmin',
)


# =============================================================================
# >> ADMIN CLASSES
# =============================================================================
@admin.register(OldPluginRelease)
class OldPluginReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'plugin',
        'version',
    )
    readonly_fields = (
        'plugin',
        'version',
        'version_notes',
        'zip_file',
    )
    search_fields = (
        'plugin__name',
        'plugin__basename',
        'plugin__owner__username',
        'plugin__contributors__username',
    )


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    exclude = (
        'zip_file',
        'version',
        'slug',
    )
    list_display = (
        'name',
        'basename',
        'owner',
    )
    list_select_related = (
        'owner',
    )
    raw_id_fields = (
        'owner',
    )
    readonly_fields = (
        'basename',
        'current_version',
        'date_created',
        'date_last_updated',
    )
    search_fields = (
        'name',
        'basename',
        'owner__username',
        'contributors__username',
    )


@admin.register(PluginImage)
class PluginImageAdmin(admin.ModelAdmin):
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
    list_display = (
        'path',
        'plugin',
    )
    readonly_fields = (
        'plugin',
    )
    search_fields = (
        'path',
        'plugin__name',
        'plugin__basename',
    )
