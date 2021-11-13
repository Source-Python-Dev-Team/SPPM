"""Mixins for common functionalities between APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectRelatedInfoMixin',
    'ProjectThroughModelMixin',
)


# =============================================================================
# MIXINS
# =============================================================================
class ProjectRelatedInfoMixin(ModelViewSet):
    """Mixin used to retrieve information for a specific project."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)

    related_model_type = None
    _project = None
    _owner = None
    _contributors = None

    @property
    def owner(self):
        """Return the project's owner."""
        if self._owner is None:
            self._owner = self.project.owner.user_id
        return self._owner

    @property
    def contributors(self):
        """Return a Queryset for the project's contributors."""
        if self._contributors is None:
            self._contributors = self.project.contributors.values_list(
                'user',
                flat=True,
            )
        return self._contributors

    @property
    def project(self):
        """Return the project for the image."""
        if self._project is not None:
            return self._project
        kwargs = self.get_project_kwargs()
        try:
            self._project = self.project_model.objects.select_related(
                'owner__user'
            ).get(**kwargs)
        except self.project_model.DoesNotExist as exception:
            raise ParseError(
                f"Invalid {self.project_type.replace('-', '_')}_slug."
            ) from exception
        return self._project

    @property
    def project_model(self):
        """Return the model to use for the project."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"project_model" attribute.'
        )

    @property
    def project_type(self):
        """Return the project's type."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"project_type" attribute.'
        )

    def get_project_kwargs(self):
        """Return the kwargs to use to filter for the project."""
        project_slug = f"{self.project_type.replace('-', '_')}_slug"
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
        """Return the name for the view."""
        if hasattr(self, 'kwargs') and self.related_model_type is not None:
            plural = 's' if self.action == 'list' else ''
            return f'{self.project} - {self.related_model_type}{plural}'
        return super().get_view_name()


class ProjectThroughModelMixin(ProjectRelatedInfoMixin):
    """Mixin for through model ViewSets."""

    authentication_classes = (SessionAuthentication,)
    http_method_names = ('get', 'post', 'delete', 'options')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    owner_only_id_access = False

    def check_permissions(self, request):
        """Only allow the owner and contributors to add data relationships."""
        if request.method not in SAFE_METHODS or self.action == 'retrieve':
            user = request.user.id
            is_contributor = user in self.contributors
            if user != self.owner and not is_contributor:
                raise PermissionDenied
            if self.owner_only_id_access and is_contributor:
                raise PermissionDenied
        return super().check_permissions(request=request)
