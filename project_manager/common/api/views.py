"""Common views for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from .mixins import ProjectRelatedInfoMixin, ProjectThroughModelMixin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectAPIView',
    'ProjectImageViewSet',
    'ProjectReleaseViewSet',
    'ProjectViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class ProjectAPIView(APIView):
    """Base Project API routes."""

    http_method_names = ('get', 'options')

    project_type = None
    extra_params = ''

    def get(self, request):
        """Return all the API routes for Projects."""
        return Response(
            data={
                'contributors': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'contributors/{self.extra_params}<{self.project_type}>/',
                'games': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'games/{self.extra_params}<{self.project_type}>/',
                'images': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'images/{self.extra_params}<{self.project_type}>/',
                'projects': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'projects/{self.extra_params}',
                'releases': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'releases/{self.extra_params}<{self.project_type}>/',
                'tags': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'tags/{self.extra_params}<{self.project_type}>/',
            }
        )


class ProjectViewSet(ModelViewSet):
    """Base ViewSet for creating, updating, and listing Projects."""

    authentication_classes = (SessionAuthentication,)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    http_method_names = ('get', 'post', 'patch', 'options')
    ordering = ('-releases__created',)
    ordering_fields = ('name', 'basename', 'modified')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    stored_contributors = None
    stored_supported_games = None
    stored_tags = None

    @property
    def creation_serializer_class(self):
        """The serializer class to use ONLY when creating a project."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"creation_serializer_class" attribute.'
        )

    def check_object_permissions(self, request, obj):
        """Only allow the owner and contributors to update the project."""
        if request.method not in SAFE_METHODS:
            user_id = request.user.id
            if (
                user_id != obj.owner.user.id and
                user_id not in obj.contributors.values_list('user', flat=True)
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
        self.store_many_to_many_fields(request=request)
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return the serializer class for the current method."""
        if self.request.method == 'POST':
            return self.creation_serializer_class
        return super().get_serializer_class()

    def store_many_to_many_fields(self, request):
        """Store the many-to-many fields."""
        self.stored_contributors = request.data.pop('contributors', None)
        self.stored_supported_games = request.data.pop('supported_games', None)
        self.stored_tags = request.data.pop('tags', None)

    def update(self, request, *args, **kwargs):
        """Store the many-to-many fields before updating."""
        self.store_many_to_many_fields(request=request)
        return super().update(request, *args, **kwargs)


class ProjectImageViewSet(ProjectThroughModelMixin):
    """Base Image View."""

    http_method_names = ('get', 'post', 'options')


class ProjectReleaseViewSet(ProjectRelatedInfoMixin):
    """Base Release ViewSet."""

    http_method_names = ('get', 'post', 'options')
    ordering = ('-created',)
    ordering_fields = ('created',)


class ProjectGameViewSet(ProjectThroughModelMixin):
    """"""

    http_method_names = ('get', 'post', 'delete', 'options')
    ordering = ('-game',)
    ordering_fields = ('game',)


class ProjectTagViewSet(ProjectThroughModelMixin):
    """"""

    http_method_names = ('get', 'post', 'delete', 'options')
    ordering = ('-tag',)
    ordering_fields = ('tag',)


class ProjectContributorViewSet(ProjectThroughModelMixin):
    """"""

    http_method_names = ('get', 'post', 'delete', 'options')
    ordering = ('-user',)
    ordering_fields = ('user',)

    owner_only = True
