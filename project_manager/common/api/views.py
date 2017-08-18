"""Common views for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectAPIView',
    'ProjectImageViewSet',
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
                'projects': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'projects/{self.extra_params}',
                'images': reverse(
                    viewname=f'api:{self.project_type}s:endpoints',
                    request=request,
                ) + f'images/{self.extra_params}<{self.project_type}>/',
            }
        )


class ProjectViewSet(ModelViewSet):
    """Base ViewSet for creating, updating, and listing Projects."""

    authentication_classes = (SessionAuthentication,)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    http_method_names = ['get', 'post', 'patch', 'options']
    ordering = ('-releases__created',)
    ordering_fields = ('name', 'basename', 'modified')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    stored_contributors = None
    stored_supported_games = None
    stored_tags = None

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

    def store_many_to_many_fields(self, request):
        """Store the many-to-many fields."""
        self.stored_contributors = request.data.pop('contributors', None)
        self.stored_supported_games = request.data.pop('supported_games', None)
        self.stored_tags = request.data.pop('tags', None)

    def update(self, request, *args, **kwargs):
        """Store the many-to-many fields before updating."""
        self.store_many_to_many_fields(request=request)
        return super().update(request, *args, **kwargs)


class ProjectImageViewSet(ModelViewSet):
    """Base Image View."""

    authentication_classes = (SessionAuthentication,)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('-created',)
    ordering_fields = ('created',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    parent_project = None
    _project = None

    @property
    def project(self):
        """Return the project for the image."""
        if self._project is not None:
            return self._project
        kwargs = self.get_project_kwargs(self.parent_project)
        try:
            self._project = self.project_model.objects.select_related(
                'owner__user'
            ).get(**kwargs)
        except self.project_model.DoesNotExist:
            raise ParseError(
                'Invalid {project_type}_slug.'.format(
                    project_type=self.project_type.replace('-', '_')
                )
            )
        return self._project

    @property
    def project_model(self):
        """Return the model to use for the project."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_model" attribute.'
        )

    @property
    def project_type(self):
        """Return the project's type."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_type" attribute.'
        )

    def check_permissions(self, request):
        if request.method not in SAFE_METHODS:
            user_id = request.user.id
            if (
                user_id != self.project.owner.user.id and
                user_id not in self.project.contributors.values_list(
                    'user',
                    flat=True,
                )
            ):
                raise PermissionDenied
        return super().check_permissions(request=request)

    def get_project_kwargs(self, parent_project=None):
        """Return the kwargs to use to filter for the project."""
        project_slug = '{project_type}_slug'.format(
            project_type=self.project_type.replace('-', '_')
        )
        return {
            'slug': self.kwargs.get(project_slug)
        }

    def get_queryset(self):
        """Filter images to only the ones of the current project."""
        queryset = super().get_queryset()
        kwargs = {
            self.project_type.replace('-', '_'): self.project
        }
        return queryset.filter(**kwargs)
