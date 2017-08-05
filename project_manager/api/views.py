# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import OrderedDict

# 3rd-Party Django
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


# =============================================================================
# >> VIEWS
# =============================================================================
class ProjectManagerAPIView(APIView):

    def get(self, request):
        data = OrderedDict([
            (
                'packages',
                reverse(
                    viewname='api:packages:endpoints',
                    request=request,
                )
            ),
            (
                'plugins',
                reverse(
                    viewname='api:plugins:endpoints',
                    request=request,
                )
            ),
            (
                'sub-plugins',
                reverse(
                    viewname='api:sub-plugins:endpoints',
                    request=request,
                )
            ),
            (
                'users',
                reverse(
                    viewname='api:users:users-list',
                    request=request,
                )
            ),
        ])

        return Response(data)
