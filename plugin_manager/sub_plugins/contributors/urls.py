# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    SubPluginAddContributorView, SubPluginAddContributorConfirmationView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/contributors/add/
        regex=r'^add/$',
        view=SubPluginAddContributorView.as_view(),
        name='add',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/contributors/add/<id>/
        regex=r'^add/(?P<id>\d+)/$',
        view=SubPluginAddContributorConfirmationView.as_view(),
        name='confirm-add',
    ),
    # url(
    #     # http://plugins.sourcepython.com/plugins/<slug>/contributors/remove/
    #     regex=r'^remove/$',
    #     view=PluginAddContributorView.as_view(),
    #     name='remove',
    # ),
    # url(
    #     # http://plugins.sourcepython.com/plugins/<slug>/contributors/remove/<id>/
    #     regex=r'^remove/(?P<id>\d+)/$',
    #     view=PluginAddContributorConfirmationView.as_view(),
    #     name='confirm-remove',
    # ),
]
