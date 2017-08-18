"""User admin classes."""

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
# >> ADMINS
# =============================================================================
@admin.register(ForumUser)
class ForumUserAdmin(admin.ModelAdmin):
    """ForumUser admin."""

    actions = None
    list_display = (
        'get_username',
        'forum_id',
    )
    readonly_fields = (
        'user',
        'forum_id',
    )
    search_fields = (
        'user__username',
    )

    def get_queryset(self, request):
        return super().get_queryset(request=request).select_related(
            'user',
        )

    @staticmethod
    def get_username(obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
