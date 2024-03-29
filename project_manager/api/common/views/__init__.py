"""Common views for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from urllib.parse import unquote

# Django
from django.db import IntegrityError
from django.db.models import Prefetch

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from project_manager.api.common.views.mixins import ProjectRelatedInfoMixin
from project_manager.constants import RELEASE_VERSION_REGEX
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectAPIView',
    'ProjectContributorViewSet',
    'ProjectGameViewSet',
    'ProjectImageViewSet',
    'ProjectReleaseViewSet',
    'ProjectTagViewSet',
    'ProjectViewSet',
)


# =============================================================================
# VIEWS
# =============================================================================
class ProjectAPIView(APIView):
    """Base Project API routes."""

    http_method_names = ('get', 'options')

    project_type = None
    views = (
        'contributors',
        'games',
        'images',
        'projects',
        'releases',
        'tags',
    )
    base_kwargs = {}

    def get(self, request):
        """Return all the API routes for Projects."""
        kwargs = self.get_project_kwargs()
        return Response(
            data={
                key: unquote(
                    reverse(
                        viewname=f'api:{self.project_type}s:{key}-list',
                        kwargs=self.base_kwargs if key == 'projects' else kwargs,
                        request=request,
                    )
                ) for key in sorted(self.views)
            }
        )

    def get_view_name(self):
        """Return the project type API name."""
        return f'{self.project_type.title()} APIs'

    def get_project_kwargs(self):
        """Return the reverse kwargs for the project."""
        key = f'{self.project_type.replace("-", "_")}_slug'
        return {
            key: f'<{self.project_type}>',
            **self.base_kwargs,
        }


class ProjectViewSet(ModelViewSet):
    """Base ViewSet for creating, updating, and listing Projects."""

    doc_string = """

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
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    http_method_names = ('get', 'post', 'patch', 'options')
    ordering = ('-updated',)
    ordering_fields = ('name', 'basename', 'updated', 'created')

    @property
    def creation_serializer_class(self):
        """Return the serializer class to use ONLY when creating a project."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"creation_serializer_class" attribute.'
        )

    def check_object_permissions(self, request, obj):
        """Only allow the owner and contributors to update the project."""
        if request.method not in SAFE_METHODS:
            user_id = request.user.id
            if (
                user_id != obj.owner.user.id and
                not obj.contributors.filter(user=user_id).exists()
            ):
                raise PermissionDenied

        return super().check_object_permissions(
            request=request,
            obj=obj,
        )

    def create(self, request, *args, **kwargs):
        """Store the many-to-many fields before creation."""
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as exception:
            raise ValidationError({
                'basename': f'{self.queryset.model.__name__} already exists. Cannot create.'
            }) from exception

    def get_serializer_class(self):
        """Return the serializer class for the current method."""
        if self.request.method == 'POST':
            return self.creation_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        """Prefetch the contributors in the list view."""
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.prefetch_related(
                Prefetch(
                    lookup='contributors',
                    queryset=ForumUser.objects.select_related(
                        'user'
                    ).only(
                        'forum_id',
                        'user__username',
                    ),
                ),
            )
        return queryset


class ProjectImageViewSet(ProjectRelatedInfoMixin):
    """Base Image View."""

    doc_string = """

    ###Available Ordering:

    *  **created** (descending) or **-created** (ascending)

        ####Example:
        `?ordering=created`

        `?ordering=-created`
    """
    ordering = ('-created',)
    ordering_fields = ('created',)
    related_model_type = 'Image'


class ProjectReleaseViewSet(ProjectRelatedInfoMixin):
    """Base Release ViewSet."""

    doc_string = """

    ###Available Ordering:

    *  **created** (descending) or **-created** (ascending)

        ####Example:
        `?ordering=created`

        `?ordering=-created`
    """
    http_method_names = ('get', 'post', 'options')
    ordering = ('-created',)
    ordering_fields = ('created', 'version')
    lookup_value_regex = RELEASE_VERSION_REGEX
    lookup_field = 'version'

    allow_retrieve_access = True
    related_model_type = 'Release'


class ProjectGameViewSet(ProjectRelatedInfoMixin):
    """Base Game Support ViewSet."""

    doc_string = """

    ###Available Ordering:

    *  **game** (descending) or **-game** (ascending)

        ####Example:
        `?ordering=game`

        `?ordering=-game`
    """
    ordering = ('-game',)
    ordering_fields = ('game',)
    related_model_type = 'Game'


class ProjectTagViewSet(ProjectRelatedInfoMixin):
    """Base Project Tag ViewSet."""

    doc_string = """

    ###Available Ordering:

    *  **tag** (descending) or **-tag** (ascending)

        ####Example:
        `?ordering=tag`

        `?ordering=-tag`
    """
    ordering = ('-tag',)
    ordering_fields = ('tag',)
    related_model_type = 'Tag'


class ProjectContributorViewSet(ProjectRelatedInfoMixin):
    """Base Project Contributor ViewSet."""

    doc_string = """

    ###Available Ordering:

    *  **user** (descending) or **-user** (ascending)

        ####Example:
        `?ordering=user`

        `?ordering=-user`
    """
    ordering = ('user',)
    ordering_fields = ('user',)
    related_model_type = 'Contributor'

    owner_only_id_access = True
