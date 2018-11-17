"""Tag views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.views import PaginatedListView
from project_manager.tags.models import Tag


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'TagListView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class TagListView(PaginatedListView):
    """Tag listing view."""

    model = Tag
    paginate_by = 20
    template_name = 'tags/list.html'
