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
    readonly_fields = (
        'username',
        'id',
    )
