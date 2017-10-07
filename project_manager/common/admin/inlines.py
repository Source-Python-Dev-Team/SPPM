"""Inline for project admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms
from django.contrib import admin
from django.db.models import Q
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectContributorInline',
    'ProjectGameInline',
    'ProjectTagInline',
)


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

    extra = 0
    fields = (
        'game',
    )

    def get_formset(self, request, obj=None, **kwargs):
        """Disallow adding/modifying Game objects in the inline."""
        formset = super().get_formset(request=request, obj=obj, **kwargs)
        widget = formset.form.base_fields['game'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        return formset


class ProjectTagInline(admin.TabularInline):
    """Base Project Tag Inline."""

    fields = (
        'tag',
    )
    readonly_fields = (
        'tag',
    )

    def has_add_permission(self, request):
        """Disallow adding new tags in the Admin."""
        return False
