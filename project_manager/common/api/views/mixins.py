"""Mixins for common functionalities between APIs."""

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
from rest_framework.viewsets import ModelViewSet


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectRelatedInfoMixin',
    'ProjectThroughModelMixin',
)


# =============================================================================
# >> MIXINS
# =============================================================================
class ProjectRelatedInfoMixin(ModelViewSet):
    """Mixin used to retrieve information for a specific project."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)

    api_type = None
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

    def get_project_kwargs(self, parent_project=None):
        """Return the kwargs to use to filter for the project."""
        project_slug = '{project_type}_slug'.format(
            project_type=self.project_type.replace('-', '_')
        )
        return {
            'slug': self.kwargs.get(project_slug)
        }

    def get_queryset(self):
        """Filter the queryset to only the ones for the current project."""
        queryset = super().get_queryset()
        kwargs = {
            self.project_type.replace('-', '_'): self.project
        }
        return queryset.filter(**kwargs)

    def get_view_name(self):
        if hasattr(self, 'kwargs') and self.api_type is not None:
            return f'{self.project} - {self.api_type}'
        return super().get_view_name()


class ProjectThroughModelMixin(ProjectRelatedInfoMixin):
    """Mixin for through model ViewSets."""

    authentication_classes = (SessionAuthentication,)
    http_method_names = ('get', 'post', 'delete', 'options')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    owner_only = False
    _owner = None
    _contributors = list()

    @property
    def owner(self):
        """Return the project's owner."""
        if self._owner is None:
            self._owner = self.project.owner.user_id
        return self._owner

    @property
    def contributors(self):
        """Return a Queryset for the project's contributors."""
        if isinstance(self._contributors, list):
            self._contributors = self.project.contributors.values_list(
                'user',
                flat=True,
            )
        return self._contributors

    def check_permissions(self, request):
        """Only allow the owner and contributors to add game support."""
        if request.method not in SAFE_METHODS or self.action == 'retrieve':
            user = request.user.id
            is_contributor = user in self.contributors
            if user != self.owner and not is_contributor:
                raise PermissionDenied
            if self.owner_only and is_contributor:
                raise PermissionDenied
        return super().check_permissions(request=request)
