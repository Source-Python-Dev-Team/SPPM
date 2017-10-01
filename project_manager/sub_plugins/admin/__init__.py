"""SubPlugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import copy

# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin
from .forms import SubPluginAdminForm
from ..models import SubPluginRelease
from ..models import SubPlugin
from ..models import SubPluginImage


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAdmin',
    'SubPluginImageAdmin',
    'SubPluginReleaseAdmin',
)


# =============================================================================
# >> GLOBALS
# =============================================================================
_project_fieldsets = copy.deepcopy(ProjectAdmin.fieldsets)
_project_fieldsets[0][1]['fields'] += ('plugin',)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(SubPlugin)
class SubPluginAdmin(ProjectAdmin):
    """SubPlugin admin."""

    fieldsets = _project_fieldsets
    form = SubPluginAdminForm
    list_display = ProjectAdmin.list_display + (
        'plugin',
    )
    raw_id_fields = ProjectAdmin.raw_id_fields + (
        'plugin',
    )
    search_fields = ProjectAdmin.search_fields + (
        'plugin__name',
        'plugin__basename',
    )


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
