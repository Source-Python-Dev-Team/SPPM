"""Tag URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from project_manager.tags.views import TagListView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'tags'

urlpatterns = [
    url(
        # /tags/
        regex=r'^$',
        view=TagListView.as_view(),
        name='list',
    ),
]
