"""User API URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# 3rd-Party Django
from rest_framework import routers

# App
from project_manager.users.api.views import ForumUserViewSet


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'',
    viewset=ForumUserViewSet,
    base_name='users'
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'users'

urlpatterns = [
    url(
        regex=r'^',
        view=include(router.urls),
    )
]
