"""Project API filters."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Q

# Third Party Django
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectFilterSet',
)


# =============================================================================
# FILTERS
# =============================================================================
class ProjectFilterSet(FilterSet):
    """Filters for Projects."""

    game = CharFilter(
        field_name='supported_games__basename',
        label='Game',
    )
    tag = CharFilter(
        field_name='tags__name',
        label='Tag',
    )
    user = CharFilter(
        method='filter_user',
        label='User',
    )

    class Meta:
        """Define metaclass attributes."""

        fields = (
            'game',
            'tag',
            'user',
        )

    @staticmethod
    def filter_user(queryset, name, value):
        """Filter to Projects owned or contributed to by given ForumUser."""
        return queryset.filter(
            Q(owner__user__username=value) |
            Q(contributors__user__username=value)
        )
