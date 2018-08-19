"""Plugin API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Prefetch

# 3rd-Party Django
from rest_framework.reverse import reverse

# App
from project_manager.common.api.views.mixins import ProjectThroughModelMixin
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from .filters import PluginFilter
from .serializers import (
    PluginContributorSerializer,
    PluginCreateSerializer,
    PluginGameSerializer,
    PluginImageSerializer,
    PluginReleaseSerializer,
    PluginSerializer,
    PluginTagSerializer,
    SubPluginPathSerializer,
)
from ..models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginReleaseDownloadRequirement,
    PluginReleasePackageRequirement,
    PluginReleasePyPiRequirement,
    PluginReleaseVersionControlRequirement,
    PluginTag,
    SubPluginPath,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAPIView',
    'PluginContributorViewSet',
    'PluginGameViewSet',
    'PluginImageViewSet',
    'PluginReleaseViewSet',
    'PluginTagViewSet',
    'PluginViewSet',
    'SubPluginPathViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PluginAPIView(ProjectAPIView):
    """Plugin API routes."""

    project_type = 'plugin'

    def get(self, request):
        """Add the 'paths' route and return all of the routes."""
        response = super().get(request=request)
        response.data['paths'] = reverse(
            viewname=f'api:{self.project_type}s:endpoints',
            request=request,
        ) + f'paths/{self.extra_params}<{self.project_type}>/'
        return response


class PluginViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing Plugins.

    ###Available Filters:
    *  **game**=*{game}*
        * Filters on supported games with exact match to slug.

        ####Example:
        `?game=csgo`

        `?game=cstrike`

    *  **tag**=*{tag}*
        * Filters on tags using exact match.

        ####Example:
        `?tag=wcs`

        `?tag=sounds`

    *  **user**=*{username}*
        * Filters on username using exact match with owner/contributors.

        ####Example:
        `?user=satoon101`

        `?user=Ayuto`

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)
    *  **basename** (descending) or **-basename** (ascending)
    *  **updated** (descending) or **-updated** (ascending)

        ####Example:
        `?ordering=basename`

        `?ordering=-updated`
    """

    filter_class = PluginFilter
    queryset = Plugin.objects.prefetch_related(
        Prefetch(
            lookup='releases',
            queryset=PluginRelease.objects.order_by(
                '-created',
            ),
        ),
    ).select_related(
        'owner__user',
    )
    serializer_class = PluginSerializer

    creation_serializer_class = PluginCreateSerializer


class PluginImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Plugins."""

    queryset = PluginImage.objects.select_related(
        'plugin',
    )
    serializer_class = PluginImageSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for Plugins."""

    queryset = PluginRelease.objects.select_related(
        'plugin',
    ).prefetch_related(
        Prefetch(
            lookup='pluginreleasepackagerequirement_set',
            queryset=PluginReleasePackageRequirement.objects.order_by(
                'package_requirement__name',
            ).select_related(
                'package_requirement',
            )
        ),
        Prefetch(
            lookup='pluginreleasedownloadrequirement_set',
            queryset=PluginReleaseDownloadRequirement.objects.order_by(
                'download_requirement__url',
            ).select_related(
                'download_requirement',
            )
        ),
        Prefetch(
            lookup='pluginreleasepypirequirement_set',
            queryset=PluginReleasePyPiRequirement.objects.order_by(
                'pypi_requirement__name',
            ).select_related(
                'pypi_requirement',
            )
        ),
        Prefetch(
            lookup='pluginreleaseversioncontrolrequirement_set',
            queryset=PluginReleaseVersionControlRequirement.objects.order_by(
                'vcs_requirement__name',
            ).select_related(
                'vcs_requirement',
            )
        ),
    )
    serializer_class = PluginReleaseSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginGameViewSet(ProjectGameViewSet):
    """Supported Games listing for Plugins."""

    queryset = PluginGame.objects.select_related(
        'game',
        'plugin',
    )
    serializer_class = PluginGameSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginTagViewSet(ProjectTagViewSet):
    """Tags listing for Plugins."""

    queryset = PluginTag.objects.select_related(
        'tag',
        'plugin',
    )
    serializer_class = PluginTagSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginContributorViewSet(ProjectContributorViewSet):
    """Contributors listing for Plugins."""

    queryset = PluginContributor.objects.select_related(
        'user__user',
        'plugin',
    )
    serializer_class = PluginContributorSerializer

    project_type = 'plugin'
    project_model = Plugin


class SubPluginPathViewSet(ProjectThroughModelMixin):
    """Sub-Plugin Paths listing."""

    http_method_names = ('get', 'post', 'patch', 'delete', 'options')
    ordering = ('path',)
    queryset = SubPluginPath.objects.select_related(
        'plugin',
    )
    serializer_class = SubPluginPathSerializer

    api_type = 'Sub-Plugin Paths'
    project_type = 'plugin'
    project_model = Plugin
