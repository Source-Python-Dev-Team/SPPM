# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from django.views.generic import ListView

# App Imports
from .models import Tag


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'TagListView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class TagListView(ListView):
    model = Tag
    paginate_by = 20
    template_name = 'tags/list.html'
