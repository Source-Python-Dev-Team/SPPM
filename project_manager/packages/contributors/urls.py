"""Package contributors URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from project_manager.packages.contributors.views import (
    PackageAddContributorView,
    PackageAddContributorConfirmationView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'contributors'

urlpatterns = [
    url(
        # /packages/<slug>/contributors/add/
        regex=r'^add/$',
        view=PackageAddContributorView.as_view(),
        name='add',
    ),
    url(
        # /packages/<slug>/contributors/add/<forum_id>/
        regex=r'^add/(?P<forum_id>\d+)/$',
        view=PackageAddContributorConfirmationView.as_view(),
        name='confirm-add',
    ),
    # url(
    #     # /packages/<slug>/contributors/remove/
    #     regex=r'^remove/$',
    #     view=PluginAddContributorView.as_view(),
    #     name='remove',
    # ),
    # url(
    #     # /packages/<slug>/contributors/remove/<forum_id>/
    #     regex=r'^remove/(?P<forum_id>\d+)/$',
    #     view=PluginAddContributorConfirmationView.as_view(),
    #     name='confirm-remove',
    # ),
]
