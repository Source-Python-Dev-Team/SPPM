"""Base App URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

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
]
