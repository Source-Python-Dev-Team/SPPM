"""Inline for project admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin


# =============================================================================
# >> INLINES
# =============================================================================
class ProjectContributorInline(admin.TabularInline):
    """Base Project Contributor Inline."""

    extra = 0
    fields = (
        'user',
    )
    raw_id_fields = (
        'user',
    )


class ProjectGameInline(admin.TabularInline):
    """Base Project Game Inline."""

    extra = 0
    fields = (
        'game',
    )


class ProjectTagInline(admin.TabularInline):
    """Base Project Tag Inline."""

    fields = (
        'tag',
    )
    readonly_fields = (
        'tag',
    )

    def has_add_permission(self, request):
        return False
