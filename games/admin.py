"""Game admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest

# App
from games.models import Game

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "GameAdmin",
)


# =============================================================================
# ADMINS
# =============================================================================
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Game admin."""

    exclude = (
        "slug",
    )
    list_display = (
        "basename",
        "name",
        "icon",
    )
    list_editable = (
        "name",
        "icon",
    )
    search_fields = (
        "name",
        "basename",
    )

    def get_readonly_fields(self, _: HttpRequest, obj: Model=None) -> tuple:
        """Allow basename to be created but not edited."""
        if obj:
            return *self.readonly_fields, "basename"

        return self.readonly_fields
