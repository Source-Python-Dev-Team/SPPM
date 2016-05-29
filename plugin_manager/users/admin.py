# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserAdmin',
)


# =============================================================================
# >> ADMIN CLASSES
# =============================================================================
@admin.register(ForumUser)
class ForumUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'id',
    )
    readonly_fields = (
        'username',
        'id',
    )
    search_fields = (
        'username',
    )
