"""User API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import include, path

# Third Party Django
from rest_framework import routers

# App
from users.api.views import ForumUserViewSet


# =============================================================================
# ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'',
    viewset=ForumUserViewSet,
    basename='users'
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'users'

urlpatterns = [
    path(
        route='',
        view=include(router.urls),
    )
]
