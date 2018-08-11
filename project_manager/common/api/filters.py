"""Project API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Q

# 3rd-Party Django
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectFilter',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class ProjectFilter(FilterSet):
    """Filters for Projects."""

    game = CharFilter(field_name='supported_games__basename')
    user = CharFilter(method='filter_user')
    tag = CharFilter(field_name='tags__name')

    class Meta:
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
