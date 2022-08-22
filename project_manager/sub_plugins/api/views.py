"""SubPlugin API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Prefetch

# Third Party Django
from rest_framework.parsers import ParseError

# App
from project_manager.api.common.views import (
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
    base_kwargs = {
        'plugin_slug': '<plugin>',
    }


class SubPluginViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing SubPlugins."""

    __doc__ += ProjectViewSet.doc_string
    filterset_class = SubPluginFilterSet
    queryset = SubPlugin.objects.select_related(
        'owner__user',
        'plugin',
    ).prefetch_related(
        Prefetch(
            lookup='releases',
            queryset=SubPluginRelease.objects.order_by(
                '-created',
            ),
        ),
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

    __doc__ += ProjectImageViewSet.doc_string
    queryset = SubPluginImage.objects.select_related(
        'sub_plugin',
    )
    serializer_class = SubPluginImageSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin


class SubPluginReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for SubPlugins."""

    __doc__ += ProjectReleaseViewSet.doc_string
    queryset = SubPluginRelease.objects.select_related(
        'sub_plugin',
        'created_by__user',
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


class SubPluginGameViewSet(ProjectGameViewSet):
    """Supported Games listing for SubPlugins."""

    __doc__ += ProjectGameViewSet.doc_string
    queryset = SubPluginGame.objects.select_related(
        'game',
        'sub_plugin',
    )
    serializer_class = SubPluginGameSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin


class SubPluginTagViewSet(ProjectTagViewSet):
    """Tags listing for SubPlugins."""

    __doc__ += ProjectTagViewSet.doc_string
    queryset = SubPluginTag.objects.select_related(
        'tag',
        'sub_plugin',
    )
    serializer_class = SubPluginTagSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin


class SubPluginContributorViewSet(ProjectContributorViewSet):
    """Contributors listing for SubPlugins."""

    __doc__ += ProjectContributorViewSet.doc_string
    queryset = SubPluginContributor.objects.select_related(
        'user__user',
        'sub_plugin',
    )
    serializer_class = SubPluginContributorSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin
