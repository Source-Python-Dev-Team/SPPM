"""API base URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import include, path

# App
from project_manager.api.views import ProjectManagerAPIView


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'api'

urlpatterns = [
    path(
        route='games/',
        view=include(
            'games.api.urls',
            namespace='games',
        ),
    ),
    path(
        route='packages/',
        view=include(
            'project_manager.packages.api.urls',
            namespace='packages',
        ),
    ),
    path(
        route='plugins/',
        view=include(
            'project_manager.plugins.api.urls',
            namespace='plugins',
        ),
    ),
    path(
        route='sub-plugins/',
        view=include(
            'project_manager.sub_plugins.api.urls',
            namespace='sub-plugins',
        ),
    ),
    path(
        route='tags/',
        view=include(
            'tags.api.urls',
            namespace='tags',
        ),
    ),
    path(
        route='users/',
        view=include(
            'users.api.urls',
            namespace='users',
        ),
    ),
    path(
        route='',
        view=ProjectManagerAPIView.as_view(),
        name='api-root',
    ),
]
