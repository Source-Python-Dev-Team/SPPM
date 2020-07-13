"""Base app models."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.pagination import PageNumberPagination


# =============================================================================
# CLASSES
# =============================================================================
class BasePagination(PageNumberPagination):
    """Base Pagination for Project Manger."""

    page_size_query_param = 'page_size'
    max_page_size = 100
