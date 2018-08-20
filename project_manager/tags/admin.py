"""Tag admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.tags.models import Tag


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
    """Tag admin."""

    actions = None
    list_display = (
        'name',
        'black_listed',
    )
    list_filter = (
        'black_listed',
    )
    list_display_links = None
    list_editable = (
        'black_listed',
    )
    readonly_fields = (
        'name',
    )

    def has_add_permission(self, request):
        """Disallow adding of tags in the Admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deletion of tags in the Admin (should use black-list)."""
        return False
