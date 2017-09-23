"""Mixins for common functionalities between APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.utils import formats

# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import ParseError
from rest_framework.viewsets import ModelViewSet


# =============================================================================
# >> MIXINS
# =============================================================================
class ProjectInfoMixin(ModelViewSet):
    """Mixin used to retrieve information for a specific project."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('-created',)
    ordering_fields = ('created',)

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


class ProjectLocaleMixin(object):
    """Mixin for getting the locale for timestamps."""

    def get_date_time_dict(self, timestamp):
        """Return a dictionary of the formatted timestamp."""
        return {
            'actual': timestamp,
            'locale': self.get_date_display(
                date=timestamp,
                date_format='DATE_FORMAT',
            ),
            'locale_short': self.get_date_display(
                date=timestamp,
                date_format='SHORT_DATE_FORMAT',
            )
        }

    @staticmethod
    def get_date_display(date, date_format):
        """Return the formatted date."""
        return formats.date_format(
            value=date,
            format=date_format,
        ) if date else date
