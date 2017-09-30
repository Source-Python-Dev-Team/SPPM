"""API base views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectManagerAPIView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class ProjectManagerAPIView(APIView):
    """Project Manager API listing."""

    @staticmethod
    def get(request):
        """Retrieve the API endpoints."""
        data = {
            'packages': reverse(
                viewname='api:packages:endpoints',
                request=request,
            ),
            'plugins': reverse(
                viewname='api:plugins:endpoints',
                request=request,
            ),
            'requirements': reverse(
                viewname='api:requirements:endpoints',
                request=request,
            ),
            'sub-plugins': reverse(
                viewname='api:sub-plugins:endpoints',
                request=request,
            ),
            'users': reverse(
                viewname='api:users:users-list',
                request=request,
            ),
        }

        return Response(data)

    def get_view_name(self):
        """Return the base API name."""
        return 'Project Manager APIs'
