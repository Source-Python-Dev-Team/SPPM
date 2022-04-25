"""Plugin model classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# Third Party Django
from model_utils.fields import AutoCreatedField
from model_utils.tracker import FieldTracker

# App
from project_manager.constants import (
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from project_manager.models.abstract import (
    AbstractUUIDPrimaryKeyModel,
    Project,
    ProjectRelease,
)
from project_manager.validators import (
    basename_validator,
    version_validator,
)
from project_manager.plugins.constants import PLUGIN_LOGO_URL, PATH_MAX_LENGTH
from project_manager.plugins.helpers import (
    handle_plugin_image_upload,
    handle_plugin_logo_upload,
    handle_plugin_zip_upload,
)
from project_manager.plugins.validators import sub_plugin_path_validator


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'Plugin',
    'PluginContributor',
    'PluginGame',
    'PluginImage',
    'PluginRelease',
    'PluginReleaseDownloadRequirement',
    'PluginReleasePackageRequirement',
    'PluginReleasePyPiRequirement',
    'PluginReleaseVersionControlRequirement',
    'PluginTag',
    'SubPluginPath',
)


# =============================================================================
# MODELS
# =============================================================================
class Plugin(Project):
    """Plugin project type model."""

    basename = models.CharField(
        max_length=PROJECT_BASENAME_MAX_LENGTH,
        validators=[basename_validator],
        unique=True,
        blank=True,
    )
    owner = models.ForeignKey(
        to='users.ForumUser',
        related_name='plugins',
        on_delete=models.SET_NULL,
        null=True,
    )
    contributors = models.ManyToManyField(
        to='users.ForumUser',
        related_name='plugin_contributions',
        through='project_manager.PluginContributor',
    )
    slug = models.SlugField(
        max_length=PROJECT_SLUG_MAX_LENGTH,
        unique=True,
        blank=True,
        primary_key=True,
    )
    supported_games = models.ManyToManyField(
        to='games.Game',
        related_name='plugins',
        through='project_manager.PluginGame',
    )
    tags = models.ManyToManyField(
        to='tags.Tag',
        related_name='plugins',
        through='project_manager.PluginTag',
    )

    handle_logo_upload = handle_plugin_logo_upload
    logo_path = PLUGIN_LOGO_URL

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'Plugin'
        verbose_name_plural = 'Plugins'

    def get_absolute_url(self):
        """Return the URL for the Plugin."""
        return reverse(
            viewname='plugins:detail',
            kwargs={
                'slug': self.slug,
            }
        )


class PluginRelease(ProjectRelease):
    """Plugin release type model."""

    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        related_name='releases',
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        to='users.ForumUser',
        related_name='plugin_releases',
        on_delete=models.SET_NULL,
        null=True,
    )
    download_requirements = models.ManyToManyField(
        to='requirements.DownloadRequirement',
        related_name='required_in_plugin_releases',
        through='project_manager.PluginReleaseDownloadRequirement',
    )
    package_requirements = models.ManyToManyField(
        to='project_manager.Package',
        related_name='required_in_plugin_releases',
        through='project_manager.PluginReleasePackageRequirement',
    )
    pypi_requirements = models.ManyToManyField(
        to='requirements.PyPiRequirement',
        related_name='required_in_plugin_releases',
        through='project_manager.PluginReleasePyPiRequirement',
    )
    vcs_requirements = models.ManyToManyField(
        to='requirements.VersionControlRequirement',
        related_name='required_in_plugin_releases',
        through='project_manager.PluginReleaseVersionControlRequirement',
    )

    handle_zip_file_upload = handle_plugin_zip_upload
    project_class = Plugin

    field_tracker = FieldTracker(
        fields=[
            'version',
        ]
    )

    class Meta(ProjectRelease.Meta):
        """Define metaclass attributes."""

        unique_together = ('plugin', 'version')
        verbose_name = 'Plugin Release'
        verbose_name_plural = 'Plugin Releases'

    @property
    def project(self):
        """Return the Plugin."""
        return self.plugin

    def get_absolute_url(self):
        """Return the URL for the PluginRelease."""
        return reverse(
            viewname='plugin-download',
            kwargs={
                'slug': self.plugin_id,
                'zip_file': self.file_name,
            }
        )


class PluginImage(AbstractUUIDPrimaryKeyModel):
    """Plugin image type model."""

    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=handle_plugin_image_upload,
    )
    created = AutoCreatedField(
        verbose_name='created',
    )

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'Plugin Image'
        verbose_name_plural = 'Plugin Images'

    def __str__(self):
        """Return the proper str value of the object."""
        return f'{self.plugin} - {self.image}'


class PluginContributor(AbstractUUIDPrimaryKeyModel):
    """Plugin contributors through model."""

    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to='users.ForumUser',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin', 'user')
        verbose_name = 'Plugin Contributor'
        verbose_name_plural = 'Plugin Contributors'

    def __str__(self):
        """Return the base string."""
        return f'{self.plugin} Contributor: {self.user}'

    def clean(self):
        """Validate that the plugin's owner cannot be a contributor."""
        if hasattr(self, 'user') and self.plugin.owner == self.user:
            raise ValidationError({
                'user': (
                    f'{self.user} is the owner and cannot be added '
                    f'as a contributor.'
                )
            })
        return super().clean()


class PluginGame(AbstractUUIDPrimaryKeyModel):
    """Plugin supported_games through model."""

    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        to='games.Game',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin', 'game')
        verbose_name = 'Plugin Game'
        verbose_name_plural = 'Plugin Games'

    def __str__(self):
        """Return the base string."""
        return f'{self.plugin} Game: {self.game}'


class PluginTag(AbstractUUIDPrimaryKeyModel):
    """Plugin tags through model."""

    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        to='tags.Tag',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin', 'tag')
        verbose_name = 'Plugin Tag'
        verbose_name_plural = 'Plugin Tags'

    def __str__(self):
        """Return the base string."""
        return f'{self.plugin} Tag: {self.tag}'


class SubPluginPath(AbstractUUIDPrimaryKeyModel):
    """Model to store SubPlugin paths for a Plugin."""

    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        related_name='paths',
        on_delete=models.CASCADE,
    )
    path = models.CharField(
        max_length=PATH_MAX_LENGTH,
        validators=[sub_plugin_path_validator],
    )
    allow_module = models.BooleanField(
        default=False,
    )
    allow_package_using_basename = models.BooleanField(
        default=False,
    )
    allow_package_using_init = models.BooleanField(
        default=False,
    )

    field_tracker = FieldTracker(
        fields=[
            'path',
        ]
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('path', 'plugin')
        verbose_name = 'SubPlugin Path'
        verbose_name_plural = 'SubPlugin Paths'

    def __str__(self):
        """Return the path."""
        return str(self.path)

    def clean(self):
        """Validate that at least one of the `allow` fields is True."""
        errors = {}
        if not any([
            self.allow_module,
            self.allow_package_using_basename,
            self.allow_package_using_init,
        ]):
            message = 'At least one of the "Allow" fields must be True.'
            errors.update({
                'allow_module': message,
                'allow_package_using_basename': message,
                'allow_package_using_init': message,
            })

        if self.field_tracker.has_changed('path'):
            new_path = self.field_tracker.current()['path']
            if self.plugin.paths.filter(path=new_path).exists():
                errors.update({
                    'path': 'Path already exists for plugin.',
                })

        if errors:
            raise ValidationError(errors)

        return super().clean()

    def get_absolute_url(self):
        """Return the SubPluginPath listing URL for the Plugin."""
        # TODO: add tests once this view is created
        return reverse(
            viewname='plugins:path_list',
            kwargs={
                'slug': self.plugin_id,
            }
        )


class PluginReleaseDownloadRequirement(AbstractUUIDPrimaryKeyModel):
    """Plugin Download Requirement for Release model."""

    plugin_release = models.ForeignKey(
        to='project_manager.PluginRelease',
        on_delete=models.CASCADE,
    )
    download_requirement = models.ForeignKey(
        to='requirements.DownloadRequirement',
        on_delete=models.CASCADE,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'download_requirement')
        verbose_name = 'Plugin Release Download Requirement'
        verbose_name_plural = 'Plugin Release Download Requirements'

    def __str__(self):
        """Return the requirement's url."""
        return self.download_requirement.url


class PluginReleasePackageRequirement(AbstractUUIDPrimaryKeyModel):
    """Plugin Package Requirement for Release model."""

    plugin_release = models.ForeignKey(
        to='project_manager.PluginRelease',
        on_delete=models.CASCADE,
    )
    package_requirement = models.ForeignKey(
        to='project_manager.Package',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the custom package for this release '
            'of the plugin.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'package_requirement')
        verbose_name = 'Plugin Release Package Requirement'
        verbose_name_plural = 'Plugin Release Package Requirements'

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.package_requirement.name} - {self.version}'


class PluginReleasePyPiRequirement(AbstractUUIDPrimaryKeyModel):
    """Plugin PyPi Requirement for Release model."""

    plugin_release = models.ForeignKey(
        to='project_manager.PluginRelease',
        on_delete=models.CASCADE,
    )
    pypi_requirement = models.ForeignKey(
        to='requirements.PyPiRequirement',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the PyPi package for this release of the plugin.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'pypi_requirement')
        verbose_name = 'Plugin Release PyPi Requirement'
        verbose_name_plural = 'Plugin Release PyPi Requirements'

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.pypi_requirement.name} - {self.version}'


class PluginReleaseVersionControlRequirement(AbstractUUIDPrimaryKeyModel):
    """Plugin VCS Requirement for Release model."""

    plugin_release = models.ForeignKey(
        to='project_manager.PluginRelease',
        on_delete=models.CASCADE,
    )
    vcs_requirement = models.ForeignKey(
        to='requirements.VersionControlRequirement',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the VCS package for this release of the plugin.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'vcs_requirement')
        verbose_name = 'Plugin Release Version Control Requirement'
        verbose_name_plural = 'Plugin Release Version Control Requirements'

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.vcs_requirement.url} - {self.version}'
