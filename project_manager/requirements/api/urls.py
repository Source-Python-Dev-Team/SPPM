# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import (
    DownloadRequirementViewSet,
    PyPiRequirementViewSet,
    RequirementAPIView,
    VersionControlRequirementViewSet,
)


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'download',
    viewset=DownloadRequirementViewSet,
    base_name='download'
)
router.register(
    prefix=r'pypi',
    viewset=PyPiRequirementViewSet,
    base_name='pypi'
)
router.register(
    prefix=r'vcs',
    viewset=VersionControlRequirementViewSet,
    base_name='vcs'
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=RequirementAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
