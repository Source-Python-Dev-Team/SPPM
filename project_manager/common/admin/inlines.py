"""Inline for project admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.db.models import Q


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectContributorInline',
    'ProjectGameInline',
    'ProjectImageInline',
    'ProjectTagInline',
)


# =============================================================================
# INLINES
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

    def get_formset(self, request, obj=None, **kwargs):
        """Disallow the owner to be a contributor."""
        formset = super().get_formset(request=request, obj=obj, **kwargs)
        queryset = formset.form.base_fields['user'].queryset
        formset.form.base_fields['user'].queryset = queryset.filter(
            ~Q(user=obj.owner.user)
        )
        return formset


class ProjectGameInline(admin.TabularInline):
    """Base Project Game Inline."""

    fields = (
        'game',
    )
    readonly_fields = (
        'game',
    )

    def get_queryset(self, request):
        return super().get_queryset(
            request=request,
        ).select_related(
            'game',
        ).order_by(
            'game__name',
        )

    def has_add_permission(self, request, obj=None):
        """Disallow adding new games in the Admin."""
        return False


class ProjectTagInline(admin.TabularInline):
    """Base Project Tag Inline."""

    fields = (
        'tag',
    )
    readonly_fields = (
        'tag',
    )

    def get_queryset(self, request):
        return super().get_queryset(
            request=request,
        ).select_related(
            'tag',
        ).order_by(
            'tag__name',
        )

    def has_add_permission(self, request, obj=None):
        """Disallow adding new tags in the Admin."""
        return False


class ProjectImageInline(admin.TabularInline):
    """Base Project Image Inline."""

    fields = (
        'image',
        'created',
    )

    readonly_fields = (
        'image',
        'created',
    )

    def has_add_permission(self, request, obj=None):
        """Disallow adding new images in the Admin."""
        return False
