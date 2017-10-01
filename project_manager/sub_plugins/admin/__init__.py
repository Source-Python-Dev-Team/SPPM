"""SubPlugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import SubPluginRelease
from .models import SubPlugin
from .models import SubPluginImage


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAdmin',
    'SubPluginImageAdmin',
    'SubPluginReleaseAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(SubPluginRelease)
class SubPluginReleaseAdmin(admin.ModelAdmin):
    """SubPluginRelease admin."""

    list_display = (
        'sub_plugin',
    )
    readonly_fields = (
        'sub_plugin',
    )
    search_fields = (
        'sub_plugin__name',
        'sub_plugin__basename',
        'sub_plugin__owner__user__username',
        'sub_plugin__contributors__user__username',
        'sub_plugin__plugin__basename',
        'sub_plugin__plugin__name',
    )


@admin.register(SubPlugin)
class SubPluginAdmin(admin.ModelAdmin):
    """SubPlugin admin."""

    exclude = (
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
    )
    search_fields = (
        'name',
        'basename',
        'owner__user__username',
        'contributors__user__username',
        'plugin__name',
        'plugin__basename',
    )


@admin.register(SubPluginImage)
class SubPluginImageAdmin(admin.ModelAdmin):
    """SubPluginImage admin."""

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

    @staticmethod
    def get_plugin(obj):
        """Return the Plugin for the SubPlugin."""
        return obj.sub_plugin.plugin
    get_plugin.short_description = 'Plugin'
    get_plugin.admin_order_field = 'sub_plugin__plugin'
