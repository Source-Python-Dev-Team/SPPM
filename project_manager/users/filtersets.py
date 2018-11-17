"""User filter sets."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet

# App
from project_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserFilterSet',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class ForumUserFilterSet(FilterSet):
    """Filter set for ForumUser."""

    username = CharFilter(
        'user__username'
    )

    class Meta:
        model = ForumUser
        fields = (
            'username',
        )
