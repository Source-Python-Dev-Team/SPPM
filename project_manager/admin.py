"""Base app admin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.contrib.auth import get_user_model


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    """User model Admin."""

    actions = None
    fields = (
        'username',
        'is_superuser',
        'is_staff',
    )

    def has_add_permission(self, request):
        """Disallow creating Users in the Admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deleting Users in the Admin."""
        return False
