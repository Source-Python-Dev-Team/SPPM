# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import Tag


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'TagAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = (
        'name',
    )