"""Plugin API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Prefetch

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
from project_manager.api.common.views.mixins import ProjectRelatedInfoMixin
from project_manager.plugins.api.filtersets import PluginFilterSet
from project_manager.plugins.api.serializers import (
    PluginContributorSerializer,
    PluginCreateSerializer,
    PluginGameSerializer,
    PluginImageSerializer,
    PluginReleaseSerializer,
    PluginSerializer,
    PluginTagSerializer,
    SubPluginPathSerializer,
)
from project_manager.plugins.models import (
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
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
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
# VIEWS
# =============================================================================
class PluginAPIView(ProjectAPIView):
    """Plugin API routes."""

    project_type = 'plugin'
    views = ProjectAPIView.views + ('paths',)


class PluginViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing Plugins."""

    __doc__ += ProjectViewSet.doc_string
    filterset_class = PluginFilterSet
    queryset = Plugin.objects.select_related(
        'owner__user',
    ).prefetch_related(
        Prefetch(
            lookup='releases',
            queryset=PluginRelease.objects.order_by(
                '-created',
            ),
        ),
        Prefetch(
            lookup='contributors',
            queryset=ForumUser.objects.select_related('user'),
        ),
    )
    serializer_class = PluginSerializer

    creation_serializer_class = PluginCreateSerializer


class PluginImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Plugins."""

    __doc__ += ProjectImageViewSet.doc_string
    queryset = PluginImage.objects.select_related(
        'plugin',
    )
    serializer_class = PluginImageSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for Plugins."""

    __doc__ += ProjectReleaseViewSet.doc_string
    queryset = PluginRelease.objects.select_related(
        'plugin',
        'created_by__user',
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
                'vcs_requirement__url',
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

    __doc__ += ProjectGameViewSet.doc_string
    queryset = PluginGame.objects.select_related(
        'game',
        'plugin',
    )
    serializer_class = PluginGameSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginTagViewSet(ProjectTagViewSet):
    """Tags listing for Plugins."""

    __doc__ += ProjectTagViewSet.doc_string
    queryset = PluginTag.objects.select_related(
        'tag',
        'plugin',
    )
    serializer_class = PluginTagSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginContributorViewSet(ProjectContributorViewSet):
    """Contributors listing for Plugins."""

    __doc__ += ProjectContributorViewSet.doc_string
    queryset = PluginContributor.objects.select_related(
        'user__user',
        'plugin',
    )
    serializer_class = PluginContributorSerializer

    project_type = 'plugin'
    project_model = Plugin


class SubPluginPathViewSet(ProjectRelatedInfoMixin):
    """Sub-Plugin Paths listing.

    ###Available Ordering:

    *  **path** (descending) or **-path** (ascending)

        ####Example:
        `?ordering=path`

        `?ordering=-path`
    """

    http_method_names = ('get', 'post', 'patch', 'delete', 'options')
    ordering = ('path',)
    queryset = SubPluginPath.objects.select_related(
        'plugin',
    )
    serializer_class = SubPluginPathSerializer

    project_type = 'plugin'
    project_model = Plugin
    related_model_type = 'Sub-Plugin Path'
