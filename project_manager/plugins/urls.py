"""Plugin URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import include, path

# App
from project_manager.plugins.views import PluginCreateView, PluginView


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'plugins'

urlpatterns = [
    path(
        # /plugins
        route='',
        view=PluginView.as_view(),
        name='list',
    ),
    path(
        # /plugins/create
        route='create',
        view=PluginCreateView.as_view(),
        name='create',
    ),
    path(
        # /plugins/<slug>
        route='<slug:slug>',
        view=PluginView.as_view(),
        name='detail',
    ),
    path(
        # /plugins/<slug>/sub-plugins
        route='<slug:slug>/sub-plugins/',
        view=include(
            'project_manager.sub_plugins.urls',
            namespace='sub-plugins',
        ),
        name='sub-plugins',
    ),
]
