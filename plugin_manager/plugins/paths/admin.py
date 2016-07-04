# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import SubPluginPath


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginPathAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
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
