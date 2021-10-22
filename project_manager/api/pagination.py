"""Base app models."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.pagination import PageNumberPagination


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'BasePagination',
)


# =============================================================================
# CLASSES
# =============================================================================
class BasePagination(PageNumberPagination):
    """Base Pagination for Project Manger."""

    page_size_query_param = 'page_size'
    max_page_size = 100
