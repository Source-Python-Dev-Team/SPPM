"""API base URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# App
from .views import ProjectManagerAPIView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^packages/',
        view=include(
            'project_manager.packages.api.urls',
            namespace='packages',
        ),
    ),
    url(
        regex=r'^plugins/',
        view=include(
            'project_manager.plugins.api.urls',
            namespace='plugins',
        ),
    ),
    url(
        regex=r'^sub-plugins/',
        view=include(
            'project_manager.sub_plugins.api.urls',
            namespace='sub-plugins',
        ),
    ),
    url(
        regex=r'^requirements/',
        view=include(
            'project_manager.requirements.api.urls',
            namespace='requirements',
        ),
    ),
    url(
        regex=r'^users/',
        view=include(
            'project_manager.users.api.urls',
            namespace='users',
        ),
    ),
    url(
        regex=r'^$',
        view=ProjectManagerAPIView.as_view(),
        name='api-root',
    ),
]
