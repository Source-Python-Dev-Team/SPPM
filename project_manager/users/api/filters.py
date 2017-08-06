"""User API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Q

# 3rd-Party Django
from django_filters.filters import BooleanFilter
from django_filters.filterset import FilterSet

from ..models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserFilter',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class ForumUserFilter(FilterSet):
    """Filters for ForumUsers."""

    has_contributions = BooleanFilter(method='filter_has_contributions')

    class Meta:
        model = ForumUser
        fields = (
            'has_contributions',
        )

    @staticmethod
    def filter_has_contributions(queryset, name, value):
        """Filter down to users that do/don't have any contributions."""
        value = not value
        return queryset.filter(
            Q(plugins__isnull=value) |
            Q(plugin_contributions__isnull=value) |
            Q(packages__isnull=value) |
            Q(package_contributions__isnull=value) |
            Q(sub_plugins__isnull=value) |
            Q(sub_plugin_contributions__isnull=value)
        )
