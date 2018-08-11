"""Plugin contributors URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    PluginAddContributorView, PluginAddContributorConfirmationView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'contributors'

urlpatterns = [
    url(
        # /plugins/<slug>/contributors/add/
        regex=r'^add/$',
        view=PluginAddContributorView.as_view(),
        name='add',
    ),
    url(
        # /plugins/<slug>/contributors/add/<forum_id>/
        regex=r'^add/(?P<forum_id>\d+)/$',
        view=PluginAddContributorConfirmationView.as_view(),
        name='confirm-add',
    ),
    # url(
    #     # /plugins/<slug>/contributors/remove/
    #     regex=r'^remove/$',
    #     view=PluginAddContributorView.as_view(),
    #     name='remove',
    # ),
    # url(
    #     # /plugins/<slug>/contributors/remove/<forum_id>/
    #     regex=r'^remove/(?P<forum_id>\d+)/$',
    #     view=PluginAddContributorConfirmationView.as_view(),
    #     name='confirm-remove',
    # ),
]
