"""User admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.contrib.auth import get_user_model

# App
from users.models import ForumUser

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "ForumUserAdmin",
    "UserAdmin",
)


# =============================================================================
# ADMINS
# =============================================================================
@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    """User model Admin."""

    actions = None
    fields = (
        "username",
        "is_superuser",
        "is_staff",
    )
    readonly_fields = (
        "username",
    )

    def has_add_permission(self, _):
        """Disallow creating Users in the Admin."""
        return False

    def has_delete_permission(self, _, __=None):
        """Disallow deleting Users in the Admin."""
        return False


@admin.register(ForumUser)
class ForumUserAdmin(admin.ModelAdmin):
    """ForumUser admin."""

    actions = None
    list_display = (
        "get_username",
        "forum_id",
    )
    readonly_fields = (
        "user",
        "forum_id",
    )
    search_fields = (
        "user__username",
    )

    def get_queryset(self, request):
        """Cache the 'user' for the queryset."""
        return super().get_queryset(request=request).select_related(
            "user",
        )

    def get_username(self, obj):
        """Return the user's username."""
        return obj.user.username
    get_username.short_description = "Username"
    get_username.admin_order_field = "user__username"

    def has_add_permission(self, _):
        """No one should be able to add users."""
        return False

    def has_delete_permission(self, _, __=None):
        """No one should be able to delete users."""
        return False
