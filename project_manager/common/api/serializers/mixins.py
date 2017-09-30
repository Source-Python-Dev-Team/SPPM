"""Mixins for common serializers."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.utils import formats

# 3rd-Party Django
from rest_framework.serializers import ModelSerializer


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectLocaleMixin',
    'ProjectReleaseCreationMixin',
    'ProjectThroughMixin',
)


# =============================================================================
# >> MIXINS
# =============================================================================
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


class ProjectThroughMixin(ModelSerializer):
    """Mixin for through model serializers."""

    def get_field_names(self, declared_fields, info):
        """Add the 'id' field if necessary."""
        field_names = super().get_field_names(
            declared_fields=declared_fields,
            info=info,
        )
        request = self.context['request']
        if request.method == 'GET':
            view = self.context['view']
            user = request.user.id
            if view.owner == user:
                return field_names + ('id',)
            if user in view.contributors and not view.owner_only:
                return field_names + ('id',)
        return field_names

    def validate(self, attrs):
        """Add the project to the validated data."""
        view = self.context['view']
        attrs[view.project_type.replace('-', '_')] = view.project
        return super().validate(attrs=attrs)
