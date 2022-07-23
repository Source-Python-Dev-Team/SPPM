"""Mixins for common functionalities between APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.utils.functional import cached_property

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectRelatedInfoMixin',
)


# =============================================================================
# MIXINS
# =============================================================================
class ProjectRelatedInfoMixin(ModelViewSet):
    """Mixin used to retrieve information for a specific project."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    http_method_names = ('get', 'post', 'delete', 'options')

    allow_retrieve_access = False
    owner_only_id_access = False
    related_model_type = None

    @cached_property
    def owner(self):
        """Return the project's owner."""
        return self.project.owner.user_id

    @cached_property
    def contributors(self):
        """Return a Queryset for the project's contributors."""
        return list(
            self.project.contributors.values_list(
                'user',
                flat=True,
            )
        )

    @cached_property
    def project(self):
        """Return the project for the image."""
        kwargs = self.get_project_kwargs()
        try:
            return self.project_model.objects.select_related(
                'owner__user'
            ).get(**kwargs)
        except self.project_model.DoesNotExist as exception:
            raise NotFound(
                detail=f"Invalid {self.project_type.replace('-', '_')}_slug.",
            ) from exception

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
        if hasattr(self, 'kwargs'):  # pragma: no branch
            plural = 's' if self.action == 'list' else ''
            return f'{self.project} - {self.related_model_type}{plural}'
        return super().get_view_name()  # pragma: no cover

    def check_object_permissions(self, request, obj):
        """Only allow the owner and contributors to delete related data.

        This is here so that the OPTIONS calls return correctly.
        """
        if request.method not in SAFE_METHODS or not self.allow_retrieve_access:
            self._check_permissions(user_id=request.user.id)

        return super().check_object_permissions(
            request=request,
            obj=obj,
        )

    def check_permissions(self, request):
        """Only allow the owner and contributors to add data relationships."""
        if request.method == 'POST':
            self._check_permissions(user_id=request.user.id)

        return super().check_permissions(request=request)

    def _check_permissions(self, user_id):
        is_contributor = user_id in self.contributors
        if user_id != self.owner and not is_contributor:
            raise PermissionDenied
        if self.owner_only_id_access and is_contributor:
            raise PermissionDenied
