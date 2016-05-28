# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.contrib import admin

# App Imports
from .models import Game


# =============================================================================
# >> ADMIN CLASSES
# =============================================================================
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    exclude = (
        'slug',
    )
    list_display = (
        'name',
        'basename',
    )
    search_fields = (
        'name',
        'basename',
    )
