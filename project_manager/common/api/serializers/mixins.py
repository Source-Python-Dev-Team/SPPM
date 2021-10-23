"""Mixins for common serializers."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.utils import formats

# Third Party Django
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectLocaleMixin',
    'ProjectReleaseCreationMixin',
    'ProjectThroughMixin',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
GROUP_QUERYSET_NAMES = {
    'custom': 'package',
    'pypi': 'pypi',
    'vcs': 'versioncontrol',
    'download': 'download',
}


# =============================================================================
# MIXINS
# =============================================================================
class ProjectLocaleMixin:
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
    requirements = None

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
        project = self.get_project(
            kwargs=kwargs,
        )
        self.validate_version(
            project=project,
            version=version,
        )
        project_basename = getattr(project, 'basename', None)

        args = (zip_file,)
        if parent_project is not None:
            args += (parent_project,)

        with self.zip_parser(*args) as zip_validator:
            self.validate_zip_file(
                zip_validator=zip_validator,
                project_basename=project_basename,
            )

            # This needs added for project creation
            attrs['basename'] = zip_validator.basename

            if project is not None:
                attrs[self.project_type.replace('-', '_')] = project

        return attrs

    def get_project(self, kwargs):
        """Return the Project for the given kwargs."""
        try:
            return self.project_class.objects.get(**kwargs)
        except self.project_class.DoesNotExist:
            return None

    def validate_version(self, project, version):
        """Validate that the version does not already exist."""
        kwargs = {
            self.project_type.replace('-', '_'): project,
            'version': version,
        }
        if self.Meta.model.objects.filter(**kwargs).exists():
            raise ValidationError({
                'version': 'Given version matches existing version.',
            })

    def validate_zip_file(self, zip_validator, project_basename):
        """Validate the files inside the zip file."""
        zip_validator.find_base_info()
        zip_validator.validate_file_paths()
        zip_validator.validate_basename()
        zip_validator.validate_base_file_in_zip()
        zip_validator.validate_requirements()
        self.requirements = zip_validator.requirements
        if project_basename not in (zip_validator.basename, None):
            raise ValidationError({
                'zip_file': (
                    f"Basename in zip '{zip_validator.basename}' does "
                    f"not match basename for {self.project_type} "
                    f"'{project_basename}'"
                )
            })

    def create(self, validated_data):
        """Update the project's updated datetime when release is created."""
        # Remove the basename before creating the release
        del validated_data['basename']

        instance = super().create(validated_data=validated_data)
        project_type = self.project_type.replace('-', '_')
        project = getattr(instance, project_type)
        self.project_class.objects.filter(
            pk=project.pk
        ).update(
            updated=instance.created,
        )
        self._create_requirements(instance)
        return instance

    def _create_requirements(self, release):
        """Create all requirements for the release."""
        if self.requirements is None:
            return

        # TODO: look into bulk_create
        project_type = release.__class__.__name__.lower()
        for group_type, group in self.requirements.items():
            self._create_group_requirements(
                release=release,
                project_type=project_type,
                group_type=group_type,
                group=group,
            )

    @staticmethod
    def _create_group_requirements(release, project_type, group_type, group):
        queryset_group_name = GROUP_QUERYSET_NAMES.get(group_type)
        if not queryset_group_name:
            # TODO: should we care if they have invalid groupings?
            pass

        for requirement in group:
            requirement_set = getattr(
                release,
                f'{project_type}{queryset_group_name}requirement_set'
            )
            requirement_set.create(**requirement)


class ProjectThroughMixin(ModelSerializer):
    """Mixin for through model serializers."""

    add_project = True

    def get_field_names(self, declared_fields, info):
        """Add the 'id' field if necessary."""
        field_names = super().get_field_names(
            declared_fields=declared_fields,
            info=info,
        )
        request = self.context['request']
        if request.method == 'GET':
            if 'view' in self.context:
                view = self.context['view']
                user = request.user.id
                if view.owner == user:
                    return field_names + ('id',)
                if user in view.contributors and not view.owner_only:
                    return field_names + ('id',)
        return field_names

    def validate(self, attrs):
        """Add the project to the validated data."""
        if self.add_project:
            view = self.context['view']
            attrs[view.project_type.replace('-', '_')] = view.project
        return super().validate(attrs=attrs)
