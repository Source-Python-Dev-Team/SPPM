# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import Plugin, PluginImage, PluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginReleaseAdmin',
    'PluginAdmin',
    'PluginImageAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(PluginRelease)
class PluginReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'plugin',
    )
    readonly_fields = (
        'plugin',
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