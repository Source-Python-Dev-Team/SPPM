"""Common views for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from project_manager.common.api.views.mixins import (
    ProjectRelatedInfoMixin,
    ProjectThroughModelMixin,
)
from project_manager.common.constants import RELEASE_VERSION_REGEX


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

    def get(self, request):
        """Return all the API routes for Projects."""
        base_path = reverse(
            viewname=f'api:{self.project_type}s:endpoints',
            request=request,
        )
        return Response(
            data={
                'contributors': base_path + f'contributors/<{self.project_type}>/',
                'games': base_path + f'games/<{self.project_type}>/',
                'images': base_path + f'images/<{self.project_type}>/',
                'projects': base_path + 'projects/',
                'releases': base_path + f'releases/<{self.project_type}>/',
                'tags': base_path + f'tags/<{self.project_type}>/',
            }
        )

    def get_view_name(self):
        """Return the project type API name."""
        return f'{self.project_type.title()} APIs'


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
    authentication_classes = (SessionAuthentication,)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    http_method_names = ('get', 'post', 'patch', 'options')
    ordering = ('-updated',)
    ordering_fields = ('name', 'basename', 'updated', 'created')
    permission_classes = (IsAuthenticatedOrReadOnly,)

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

    def check_permissions(self, request):
        """Only allow users who have a ForumUser to create projects."""
        if request.method not in SAFE_METHODS:
            if not hasattr(request.user, 'forum_user'):
                raise PermissionDenied
        return super().check_permissions(request=request)

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


class ProjectImageViewSet(ProjectThroughModelMixin):
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
    related_model_type = 'Release'

    def check_permissions(self, request):
        """Only allow the owner and contributors to create releases."""
        if request.method not in SAFE_METHODS:
            if not hasattr(request.user, 'forum_user'):
                raise PermissionDenied

            user = request.user.id
            is_contributor = user in self.contributors
            if user != self.owner and not is_contributor:
                raise PermissionDenied

        return super().check_permissions(request=request)


class ProjectGameViewSet(ProjectThroughModelMixin):
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


class ProjectTagViewSet(ProjectThroughModelMixin):
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


class ProjectContributorViewSet(ProjectThroughModelMixin):
    """Base Project Contributor ViewSet."""

    doc_string = """

    ###Available Ordering:

    *  **user** (descending) or **-user** (ascending)

        ####Example:
        `?ordering=user`

        `?ordering=-user`
    """
    ordering = ('-user',)
    ordering_fields = ('user',)
    related_model_type = 'Contributor'

    owner_only_id_access = True
