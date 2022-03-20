"""Tag admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from tags.models import Tag


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'TagAdmin',
)


# =============================================================================
# ADMINS
# =============================================================================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""

    actions = None
    list_display = (
        'name',
        'black_listed',
        'creator',
    )
    list_display_links = None
    list_filter = (
        'black_listed',
    )
    list_editable = (
        'black_listed',
        'creator',
    )
    raw_id_fields = (
        'creator',
    )
    readonly_fields = (
        'name',
    )

    def get_queryset(self, request):
        """Cache the 'creator' for the queryset."""
        return super().get_queryset(
            request=request,
        ).select_related(
            'creator__user',
        )

    def has_add_permission(self, request):
        """Disallow adding of tags in the Admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deletion of tags in the Admin (should use black-list)."""
        return False
