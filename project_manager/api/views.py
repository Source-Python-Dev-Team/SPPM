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
# VIEWS
# =============================================================================
class ProjectManagerAPIView(APIView):

    def get(self, request):
        data = OrderedDict([
            (
                'packages',
                reverse(
                    viewname='api:packages:packages-list',
                    request=request,
                )
            ),
            (
                'plugins',
                reverse(
                    viewname='api:plugins:plugins-list',
                    request=request,
                )
            ),
            (
                'sub-plugins',
                reverse(
                    viewname='api:sub-plugins:sub-plugins-list',
                    request=request,
                )
            )
        ])

        return Response(data)
