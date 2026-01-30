"""User custom ordering filters."""
# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import QuerySet
from django.views import View

# Third Party Django
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "ForumUserOrderingFilter",
)


# =============================================================================
# ORDERING
# =============================================================================
class ForumUserOrderingFilter(OrderingFilter):
    """Custom ForumUser ordering filter."""

    def get_ordering(
        self,
        request: Request,
        queryset: QuerySet,
        view: View,
    ) -> tuple:
        """Allow username in place of user__username."""
        ordering = list(super().get_ordering(request, queryset, view))
        for index, item in enumerate(ordering):
            prefix = "-" if item.startswith("-") else ""
            item_name = item[1:] if prefix == "-" else item
            if item_name == "username":
                ordering[index] = f"{prefix}user__username"

        return tuple(ordering)
