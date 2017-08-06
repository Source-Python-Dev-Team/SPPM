"""SubPlugin API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Q

# 3rd-Party Django
from django_filters.filters import CharFilter, NumberFilter
from django_filters.filterset import FilterSet

from ..models import SubPlugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginFilter',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class SubPluginFilter(FilterSet):
    """Filters for SubPlugins."""

    game = CharFilter(
        'supported_games__basename',
    )
    userid = NumberFilter(method='filter_userid')

    class Meta:
        model = SubPlugin
        fields = ('game',)

    @staticmethod
    def filter_userid(queryset, name, value):
        """Filter to SubPlugins owned or contributed to by given ForumUser."""
        return queryset.filter(
            Q(owner__id=value) | Q(contributors__id=value)
        )
