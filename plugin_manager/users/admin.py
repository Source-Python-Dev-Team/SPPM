# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.contrib import admin

# App Imports
from .models import ForumUser


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
