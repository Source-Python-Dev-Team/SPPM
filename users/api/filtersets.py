"""User API filters."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Count, Q

# Third Party Django
from django_filters.filters import BooleanFilter
from django_filters.filterset import FilterSet

from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserFilterSet',
)


# =============================================================================
# FILTERS
# =============================================================================
class ForumUserFilterSet(FilterSet):
    """Filters for ForumUsers."""

    has_contributions = BooleanFilter(
        method='filter_has_contributions',
        label='Has Contributions',
    )

    class Meta:
        """Define metaclass attributes."""

        model = ForumUser
        fields = (
            'has_contributions',
        )

    @staticmethod
    def filter_has_contributions(queryset, name, value):
        """Filter down to users that do/don't have any contributions."""
        queryset = queryset.annotate(
            plugin_count=Count('plugins'),
            plugin_contribution_count=Count('plugin_contributions'),
            package_count=Count('packages'),
            package_contribution_count=Count('package_contributions'),
            sub_plugin_count=Count('sub_plugins'),
            sub_plugin_contribution_count=Count('sub_plugin_contributions'),
        )
        method = queryset.filter if value else queryset.exclude
        return method(
            Q(plugin_count__gt=0) |
            Q(plugin_contribution_count__gt=0) |
            Q(package_count__gt=0) |
            Q(package_contribution_count__gt=0) |
            Q(sub_plugin_count__gt=0) |
            Q(sub_plugin_contribution_count__gt=0)
        ).distinct()
