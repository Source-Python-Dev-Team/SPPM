# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.contrib import admin

# App Imports
from .models import OldSubPluginRelease
from .models import SubPlugin
from .models import SubPluginImage


# =============================================================================
# >> ADMIN CLASSES
# =============================================================================
@admin.register(OldSubPluginRelease)
class OldSubPluginReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'sub_plugin',
        'version',
    )
    readonly_fields = (
        'sub_plugin',
        'version',
        'version_notes',
        'zip_file',
    )
    search_fields = (
        'sub_plugin__name',
        'sub_plugin__basename',
        'sub_plugin__owner__username',
        'sub_plugin__contributors__username',
        'sub_plugin__plugin__basename',
        'sub_plugin__plugin__name',
    )


@admin.register(SubPlugin)
class SubPluginAdmin(admin.ModelAdmin):
    exclude = (
        'zip_file',
        'version',
        'slug',
    )
    list_display = (
        'name',
        'basename',
        'owner',
        'plugin',
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
        'plugin__name',
        'plugin__basename',
    )


@admin.register(SubPluginImage)
class SubPluginImageAdmin(admin.ModelAdmin):
    list_display = (
        'sub_plugin',
        'get_plugin',
        'image',
    )
    readonly_fields = (
        'sub_plugin',
    )
    search_fields = (
        'sub_plugin__name',
        'sub_plugin__basename',
        'sub_plugin__plugin__name',
        'sub_plugin__plugin__basename',
    )

    def get_plugin(self, obj):
        return obj.sub_plugin.plugin
    get_plugin.short_description = 'Plugin'
    get_plugin.admin_order_field = 'sub_plugin__plugin'
