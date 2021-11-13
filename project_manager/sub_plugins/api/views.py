"""SubPlugin API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Prefetch

# Third Party Django
from rest_framework.parsers import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse

# App
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.api.filtersets import SubPluginFilterSet
from project_manager.sub_plugins.api.serializers import (
    SubPluginContributorSerializer,
    SubPluginCreateSerializer,
    SubPluginGameSerializer,
    SubPluginImageSerializer,
    SubPluginReleaseSerializer,
    SubPluginSerializer,
    SubPluginTagSerializer,
)
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
    SubPluginTag,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAPIView',
    'SubPluginContributorViewSet',
    'SubPluginGameViewSet',
    'SubPluginImageViewSet',
    'SubPluginReleaseViewSet',
    'SubPluginTagViewSet',
    'SubPluginViewSet',
)


# =============================================================================
# VIEWS
# =============================================================================
class SubPluginAPIView(ProjectAPIView):
    """SubPlugin API routes."""

    project_type = 'sub-plugin'

    def get(self, request):
        """Return all the API routes for Projects."""
        base_path = reverse(
            viewname=f'api:{self.project_type}s:endpoints',
            request=request,
        )
        return Response(
            data={
                'contributors': base_path + f'contributors/<plugin>/<{self.project_type}>/',
                'games': base_path + f'games/<plugin>/<{self.project_type}>/',
                'images': base_path + f'images/<plugin>/<{self.project_type}>/',
                'projects': base_path + 'projects/<plugin>/',
                'releases': base_path + f'releases/<plugin>/<{self.project_type}>/',
                'tags': base_path + f'tags/<plugin>/<{self.project_type}>/',
            }
        )


class SubPluginViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing SubPlugins.

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
    *  **created** (descending) or **-created** (ascending)
    *  **updated** (descending) or **-updated** (ascending)

        ####Example:
        `?ordering=basename`

        `?ordering=-updated`
    """

    filterset_class = SubPluginFilterSet
    queryset = SubPlugin.objects.prefetch_related(
        Prefetch(
            lookup='releases',
            queryset=SubPluginRelease.objects.order_by(
                '-created',
            ),
        ),
    ).select_related(
        'owner__user',
        'plugin',
    )
    serializer_class = SubPluginSerializer
    lookup_field = 'slug'

    creation_serializer_class = SubPluginCreateSerializer
    plugin = None

    def get_queryset(self):
        """Filter down to only SubPlugins for the given Plugin."""
        queryset = super().get_queryset()
        if self.plugin is not None:
            return queryset.filter(plugin=self.plugin)
        plugin_slug = self.kwargs.get('plugin_slug')
        try:
            self.plugin = Plugin.objects.get(slug=plugin_slug)
            return queryset.filter(plugin=self.plugin)
        except Plugin.DoesNotExist as exception:
            raise ParseError('Invalid plugin_slug.') from exception


class SubPluginImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for SubPlugins."""

    queryset = SubPluginImage.objects.select_related(
        'sub_plugin',
    )
    serializer_class = SubPluginImageSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin

    @property
    def parent_project(self):
        """Return the Plugin for the SubPlugin image view."""
        plugin_slug = self.kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist as exception:
            raise ParseError(
                f"Plugin '{plugin_slug}' not found."
            ) from exception
        return plugin

    def get_project_kwargs(self):
        """Add the Plugin to the kwargs for filtering for the project."""
        kwargs = super().get_project_kwargs()
        kwargs.update(
            plugin=self.parent_project,
        )
        return kwargs


class SubPluginReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for SubPlugins."""

    queryset = SubPluginRelease.objects.select_related(
        'sub_plugin',
    ).prefetch_related(
        Prefetch(
            lookup='subpluginreleasepackagerequirement_set',
            queryset=SubPluginReleasePackageRequirement.objects.order_by(
                'package_requirement__name',
            ).select_related(
                'package_requirement',
            )
        ),
        Prefetch(
            lookup='subpluginreleasedownloadrequirement_set',
            queryset=SubPluginReleaseDownloadRequirement.objects.order_by(
                'download_requirement__url',
            ).select_related(
                'download_requirement',
            )
        ),
        Prefetch(
            lookup='subpluginreleasepypirequirement_set',
            queryset=SubPluginReleasePyPiRequirement.objects.order_by(
                'pypi_requirement__name',
            ).select_related(
                'pypi_requirement',
            )
        ),
        Prefetch(
            lookup='subpluginreleaseversioncontrolrequirement_set',
            queryset=(
                SubPluginReleaseVersionControlRequirement.objects.order_by(
                    'vcs_requirement__url',
                ).select_related(
                    'vcs_requirement',
                )
            )
        ),
    )
    serializer_class = SubPluginReleaseSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin

    @property
    def parent_project(self):
        """Return the Plugin for the SubPlugin image view."""
        plugin_slug = self.kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist as exception:
            raise ParseError(
                f"Plugin '{plugin_slug}' not found."
            ) from exception
        return plugin

    def get_project_kwargs(self):
        """Add the Plugin to the kwargs for filtering for the project."""
        kwargs = super().get_project_kwargs()
        kwargs.update(
            plugin=self.parent_project,
        )
        return kwargs


class SubPluginGameViewSet(ProjectGameViewSet):
    """Supported Games listing for SubPlugins."""

    queryset = SubPluginGame.objects.select_related(
        'game',
        'sub_plugin',
    )
    serializer_class = SubPluginGameSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin


class SubPluginTagViewSet(ProjectTagViewSet):
    """Tags listing for SubPlugins."""

    queryset = SubPluginTag.objects.select_related(
        'tag',
        'sub_plugin',
    )
    serializer_class = SubPluginTagSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin


class SubPluginContributorViewSet(ProjectContributorViewSet):
    """Contributors listing for SubPlugins."""

    queryset = SubPluginContributor.objects.select_related(
        'user__user',
        'sub_plugin',
    )
    serializer_class = SubPluginContributorSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin
