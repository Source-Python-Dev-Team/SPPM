"""Forms for use with Packages."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now

# App
from project_manager.common.mixins import SubmitButtonMixin
from project_manager.packages.helpers import get_package_basename
from project_manager.packages.models import Package, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageCreateForm',
    'PackageEditForm',
    'PackageSelectGamesForm',
    'PackageUpdateForm',
)


# =============================================================================
# >> FORMS
# =============================================================================
class PackageCreateForm(SubmitButtonMixin):
    """Package creation form."""

    version = forms.CharField(
        max_length=8,
        help_text=PackageRelease._meta.get_field('version').help_text,
    )
    version_notes = forms.CharField(
        max_length=512,
        required=False,
        help_text=PackageRelease._meta.get_field('notes').help_text,
        widget=forms.Textarea(
            attrs={
                'cols': '64',
                'rows': '8',
            }
        )
    )
    zip_file = forms.FileField(
        help_text=PackageRelease._meta.get_field('zip_file').help_text,
    )

    class Meta:
        """Define metaclass attributes."""

        model = Package
        fields = (
            'name',
            'synopsis',
            'description',
            'configuration',
            'logo',
            'slug',
        )
        widgets = {
            'synopsis': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '2',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
            'configuration': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
            'slug': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        self.owner = kwargs.pop('owner')
        super().__init__(*args, **kwargs)
        old_fields = self.fields
        self.fields = {
            x: old_fields.pop(x) for x in [
                'name', 'version', 'version_notes', 'zip_file', 'synopsis',
                'description', 'configuration', 'logo',
            ]
        }
        self.fields.update(old_fields)

    def save(self, commit=True):
        """Save the package and create the release."""
        created = now()
        self.instance.created = self.instance.updated = created
        self.instance.owner = self.owner
        instance = super().save(commit)
        PackageRelease.objects.create(
            package=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['version_notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

    def clean_zip_file(self):
        """Verify the zip file contents."""
        zip_file = self.cleaned_data['zip_file']
        basename = get_package_basename(zip_file)
        if Package.objects.filter(basename=basename).exists():
            raise ValidationError(
                message=f'Package {basename} is already registered.',
                code='duplicate',
            )
        self.instance.basename = basename
        return zip_file


class PackageEditForm(SubmitButtonMixin):
    """Package field editing form."""

    class Meta:
        """Define metaclass attributes."""

        model = Package
        fields = (
            'synopsis',
            'description',
            'configuration',
            'logo',
        )
        widgets = {
            'synopsis': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '2',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
            'configuration': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
        }


class PackageSelectGamesForm(SubmitButtonMixin):
    """Package Game selection form."""

    class Meta:
        """Define metaclass attributes."""

        model = Package
        fields = (
            'supported_games',
        )
        widgets = {
            'supported_games': forms.CheckboxSelectMultiple()
        }


class PackageUpdateForm(SubmitButtonMixin):
    """Package release creation form."""

    class Meta:
        """Define metaclass attributes."""

        model = PackageRelease
        fields = (
            'version',
            'notes',
            'zip_file',
        )
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '8',
                }
            )
        }

    def save(self, commit=True):
        """Create the release."""
        instance = super().save(commit)
        PackageRelease.objects.create(
            package=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

    def clean_version(self):
        """Verify the version doesn't already exist."""
        all_versions = PackageRelease.objects.filter(
            package=self.instance
        ).values_list('version', flat=True)
        version = self.cleaned_data['version']
        if version in all_versions:
            raise ValidationError(
                message=f'Release version "{version}" already exists.',
                code='duplicate',
            )
        return version

    def clean_zip_file(self):
        """Verify the zip file contents."""
        zip_file = self.cleaned_data['zip_file']
        basename = get_package_basename(zip_file)
        if basename != self.instance.basename:
            raise ValidationError(
                message='Uploaded package does not match current package.',
                code='mismatch',
            )
        return zip_file
