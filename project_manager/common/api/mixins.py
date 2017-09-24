"""Mixins for common functionalities between APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.utils import formats

# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import ParseError
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


# =============================================================================
# >> MIXINS
# =============================================================================
class ProjectRelatedInfoMixin(ModelViewSet):
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
                date_format='DATETIME_FORMAT',
            ),
            'locale_short': self.get_date_display(
                date=timestamp,
                date_format='SHORT_DATETIME_FORMAT',
            )
        }

    @staticmethod
    def get_date_display(date, date_format):
        """Return the formatted date."""
        return formats.date_format(
            value=date,
            format=date_format,
        ) if date else date


class ProjectReleaseCreationMixin(ModelSerializer):
    """Mixin for validation/creation of a project release."""

    parent_project = None

    @property
    def project_class(self):
        """Return the project's class."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_class" attribute.'
        )

    @property
    def project_type(self):
        """Return the project's type."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_type" attribute.'
        )

    @property
    def zip_parser(self):
        """Return the project's zip parsing function."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"zip_parser" attribute.'
        )

    def get_project_kwargs(self, parent_project=None):
        """Return kwargs for the project."""
        return {
            'pk': self.context['view'].kwargs.get('pk')
        }

    def validate(self, attrs):
        """Validate that the new release can be created."""
        version = attrs.get('version', '')
        zip_file = attrs.get('zip_file')
        if any([version, zip_file]) and not all([version, zip_file]):
            raise ValidationError({
                '__all__': (
                    "If either 'version' or 'zip_file' are provided, "
                    "must be provided."
                )
            })

        # Validate the version is new for the project
        parent_project = self.parent_project
        kwargs = self.get_project_kwargs(parent_project)
        try:
            project = self.project_class.objects.get(**kwargs)
            project_basename = project.basename
        except self.project_class.DoesNotExist:
            project_basename = None
            project = None
        else:
            kwargs = {
                '{project_type}'.format(
                    project_type=self.project_type.replace('-', '_')
                ): project,
                'version': version,
            }
            if self.Meta.model.objects.filter(**kwargs).exists():
                raise ValidationError({
                    'version': 'Given version matches existing version.',
                })

        args = (zip_file,)
        if parent_project is not None:
            args += (parent_project,)
        basename = self.zip_parser(*args)
        if project_basename not in (basename, None):
            raise ValidationError({
                'zip_file': (
                    f"Basename in zip '{basename}' does not match basename "
                    f"for {self.project_type} '{project_basename}'"
                )
            })

        # This needs added for project creation
        attrs['basename'] = basename

        if project is not None:
            attrs[self.project_type.replace('-', '_')] = project
        return attrs

    def create(self, validated_data):
        """Update the project's modified datetime when release is created."""
        # Remove the basename before creating the release
        del validated_data['basename']

        instance = super().create(validated_data=validated_data)
        project_type = self.project_type.replace('-', '_')
        project = getattr(instance, project_type)
        self.project_class.objects.filter(
            pk=project.pk
        ).update(
            modified=instance.created,
        )
        return instance
