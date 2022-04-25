"""Base App URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# App
from project_manager.sub_plugins.views import (
    SubPluginCreateView,
    SubPluginView,
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'sub-plugins'

urlpatterns = [
    path(
        # /plugins/<slug>/sub-plugins
        route='',
        view=SubPluginView.as_view(),
        name='list',
    ),
    path(
        # /plugins/<slug>/sub-plugins/create
        route='create',
        view=SubPluginCreateView.as_view(),
        name='create',
    ),
    path(
        # /plugins/<slug>/sub-plugins/<sub_plugin_slug>
        route='<slug:sub_plugin_slug>',
        view=SubPluginView.as_view(),
        name='detail',
    ),
]
