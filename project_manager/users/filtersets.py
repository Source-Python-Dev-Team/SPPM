"""User filter sets."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.filterset import FilterSet

# App
from .models import ForumUser


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

    class Meta:
        model = ForumUser
        fields = ['username']
        # order_by = ['username']
