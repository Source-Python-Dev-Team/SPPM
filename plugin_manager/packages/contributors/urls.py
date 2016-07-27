# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    PackageAddContributorView, PackageAddContributorConfirmationView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # /packages/<slug>/contributors/add/
        regex=r'^add/$',
        view=PackageAddContributorView.as_view(),
        name='add',
    ),
    url(
        # /packages/<slug>/contributors/add/<id>/
        regex=r'^add/(?P<id>\d+)/$',
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
    #     # /packages/<slug>/contributors/remove/<id>/
    #     regex=r'^remove/(?P<id>\d+)/$',
    #     view=PluginAddContributorConfirmationView.as_view(),
    #     name='confirm-remove',
    # ),
]
