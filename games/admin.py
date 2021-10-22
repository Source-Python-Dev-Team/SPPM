"""Game admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from games.models import Game


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GameAdmin',
)


# =============================================================================
# ADMINS
# =============================================================================
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Game admin."""

    exclude = (
        'slug',
    )
    list_display = (
        'basename',
        'name',
        'icon',
    )
    list_editable = (
        'name',
        'icon',
    )
    readonly_fields = (
        'basename',
    )
    search_fields = (
        'name',
        'basename',
    )
