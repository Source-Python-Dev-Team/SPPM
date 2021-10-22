"""Tag API filters."""

# =============================================================================
# IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.filterset import FilterSet

# App
from tags.models import Tag


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'TagFilterSet',
)


# =============================================================================
# FILTERS
# =============================================================================
class TagFilterSet(FilterSet):
    """Filters for Tags."""

    class Meta:
        """Define metaclass attributes."""

        fields = (
            'black_listed',
        )
        model = Tag
