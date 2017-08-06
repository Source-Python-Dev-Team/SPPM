"""Package API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Q

# 3rd-Party Django
from django_filters.filters import CharFilter, NumberFilter
from django_filters.filterset import FilterSet

from ..models import Package


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageFilter',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class PackageFilter(FilterSet):
    """Filters for Packages."""

    game = CharFilter(
        'supported_games__basename',
    )
    userid = NumberFilter(method='filter_userid')

    class Meta:
        model = Package
        fields = ('game',)

    @staticmethod
    def filter_userid(queryset, name, value):
        """Filter to Packages owned or contributed to by given ForumUser."""
        return queryset.filter(
            Q(owner__id=value) | Q(contributors__id=value)
        )
