# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import (
    DownloadRequirementViewSet,
    PyPiRequirementViewSet,
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
        regex=r'^',
        view=include(router.urls),
    )
]
