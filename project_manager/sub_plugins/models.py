"""SubPlugin model classes."""

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
from project_manager.sub_plugins.constants import SUB_PLUGIN_LOGO_URL
from project_manager.sub_plugins.helpers import (
    handle_sub_plugin_image_upload,
    handle_sub_plugin_logo_upload,
    handle_sub_plugin_zip_upload,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPlugin',
    'SubPluginContributor',
    'SubPluginGame',
    'SubPluginImage',
    'SubPluginRelease',
    'SubPluginReleaseDownloadRequirement',
    'SubPluginReleasePackageRequirement',
    'SubPluginReleasePyPiRequirement',
    'SubPluginReleaseVersionControlRequirement',
    'SubPluginTag',
)


# =============================================================================
# MODELS
# =============================================================================
class SubPlugin(Project):
    """SubPlugin project type model."""

    id = models.CharField(
        max_length=PROJECT_SLUG_MAX_LENGTH * 2 + 1,
        blank=True,
        primary_key=True,
    )
    basename = models.CharField(
        max_length=PROJECT_BASENAME_MAX_LENGTH,
        validators=[basename_validator],
        blank=True,
    )
    owner = models.ForeignKey(
        to='users.ForumUser',
        related_name='sub_plugins',
        on_delete=models.SET_NULL,
        null=True,
    )
    contributors = models.ManyToManyField(
        to='users.ForumUser',
        related_name='sub_plugin_contributions',
        through='project_manager.SubPluginContributor',
    )
    slug = models.SlugField(
        max_length=PROJECT_SLUG_MAX_LENGTH,
        blank=True,
    )
    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        related_name='sub_plugins',
        on_delete=models.CASCADE,
    )
    supported_games = models.ManyToManyField(
        to='games.Game',
        related_name='sub_plugins',
        through='project_manager.SubPluginGame',
    )
    tags = models.ManyToManyField(
        to='tags.Tag',
        related_name='sub_plugins',
        through='project_manager.SubPluginTag',
    )

    handle_logo_upload = handle_sub_plugin_logo_upload
    logo_path = SUB_PLUGIN_LOGO_URL

    class Meta:
        """Define metaclass attributes."""

        unique_together = (
            ('plugin', 'basename'),
            ('plugin', 'name'),
            ('plugin', 'slug'),
        )
        verbose_name = 'SubPlugin'
        verbose_name_plural = 'SubPlugins'

    def __str__(self):
        """Return the string formatted name for the sub-plugin."""
        return f'{self.plugin.name}: {self.name}'

    def get_absolute_url(self):
        """Return the URL for the SubPlugin."""
        # TODO: add tests once this view is created
        return reverse(
            viewname='plugins:sub-plugins:detail',
            kwargs={
                'slug': self.plugin.slug,
                'sub_plugin_slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
        """Set the id using the plugin's slug and the sub_plugin's slug."""
        self.id = f'{self.plugin.slug}.{self.get_slug_value()}'
        super().save(*args, **kwargs)


class SubPluginRelease(ProjectRelease):
    """SubPlugin release type model."""

    sub_plugin = models.ForeignKey(
        to='project_manager.SubPlugin',
        related_name='releases',
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        to='users.ForumUser',
        related_name='sub_plugin_releases',
        on_delete=models.SET_NULL,
        null=True,
    )
    download_requirements = models.ManyToManyField(
        to='requirements.DownloadRequirement',
        related_name='required_in_sub_plugin_releases',
        through='project_manager.SubPluginReleaseDownloadRequirement',
    )
    package_requirements = models.ManyToManyField(
        to='project_manager.Package',
        related_name='required_in_sub_plugin_releases',
        through='project_manager.SubPluginReleasePackageRequirement',
    )
    pypi_requirements = models.ManyToManyField(
        to='requirements.PyPiRequirement',
        related_name='required_in_sub_plugin_releases',
        through='project_manager.SubPluginReleasePyPiRequirement',
    )
    vcs_requirements = models.ManyToManyField(
        to='requirements.VersionControlRequirement',
        related_name='required_in_sub_plugin_releases',
        through='project_manager.SubPluginReleaseVersionControlRequirement',
    )

    handle_zip_file_upload = handle_sub_plugin_zip_upload
    project_class = SubPlugin

    field_tracker = FieldTracker(
        fields=[
            'version',
        ]
    )

    class Meta(ProjectRelease.Meta):
        """Define metaclass attributes."""

        unique_together = ('sub_plugin', 'version')
        verbose_name = 'SubPlugin Release'
        verbose_name_plural = 'SubPlugin Releases'

    @property
    def project(self):
        """Return the SubPlugin."""
        return self.sub_plugin

    def get_absolute_url(self):
        """Return the URL for the SubPluginRelease."""
        return reverse(
            viewname='sub-plugin-download',
            kwargs={
                'slug': self.sub_plugin.plugin.slug,
                'sub_plugin_slug': self.sub_plugin.slug,
                'zip_file': self.file_name,
            }
        )


class SubPluginImage(AbstractUUIDPrimaryKeyModel):
    """SubPlugin image type model."""

    sub_plugin = models.ForeignKey(
        to='project_manager.SubPlugin',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=handle_sub_plugin_image_upload,
    )
    created = AutoCreatedField(
        verbose_name='created',
    )

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'SubPlugin Image'
        verbose_name_plural = 'SubPlugin Images'

    def __str__(self):
        """Return the proper str value of the object."""
        return f'{self.sub_plugin} - {self.image}'


class SubPluginContributor(AbstractUUIDPrimaryKeyModel):
    """SubPlugin contributors through model."""

    sub_plugin = models.ForeignKey(
        to='project_manager.SubPlugin',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to='users.ForumUser',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('sub_plugin', 'user')
        verbose_name = 'SubPlugin Contributor'
        verbose_name_plural = 'SubPlugin Contributors'

    def __str__(self):
        """Return the base string."""
        return f'{self.sub_plugin} Contributor: {self.user}'

    def clean(self):
        """Validate that the sub_plugin's owner cannot be a contributor."""
        if hasattr(self, 'user') and self.sub_plugin.owner == self.user:
            raise ValidationError({
                'user': (
                    f'{self.user} is the owner and cannot be added '
                    f'as a contributor.'
                )
            })
        return super().clean()


class SubPluginGame(AbstractUUIDPrimaryKeyModel):
    """SubPlugin supported_games through model."""

    sub_plugin = models.ForeignKey(
        to='project_manager.SubPlugin',
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        to='games.Game',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('sub_plugin', 'game')
        verbose_name = 'SubPlugin Game'
        verbose_name_plural = 'SubPlugin Games'

    def __str__(self):
        """Return the base string."""
        return f'{self.sub_plugin} Game: {self.game}'


class SubPluginTag(AbstractUUIDPrimaryKeyModel):
    """SubPlugin tags through model."""

    sub_plugin = models.ForeignKey(
        to='project_manager.SubPlugin',
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        to='tags.Tag',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('sub_plugin', 'tag')
        verbose_name = 'SubPlugin Tag'
        verbose_name_plural = 'SubPlugin Tags'

    def __str__(self):
        """Return the base string."""
        return f'{self.sub_plugin} Tag: {self.tag}'


class SubPluginReleaseDownloadRequirement(AbstractUUIDPrimaryKeyModel):
    """SubPlugin Download Requirement for Release model."""

    sub_plugin_release = models.ForeignKey(
        to='project_manager.SubPluginRelease',
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

        unique_together = ('sub_plugin_release', 'download_requirement')
        verbose_name = 'SubPlugin Release Download Requirement'
        verbose_name_plural = 'SubPlugin Release Download Requirements'

    def __str__(self):
        """Return the requirement's url."""
        return self.download_requirement.url


class SubPluginReleasePackageRequirement(AbstractUUIDPrimaryKeyModel):
    """SubPlugin Package Requirement for Release model."""

    sub_plugin_release = models.ForeignKey(
        to='project_manager.SubPluginRelease',
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
            'of the sub_plugin.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('sub_plugin_release', 'package_requirement')
        verbose_name = 'SubPlugin Release Package Requirement'
        verbose_name_plural = 'SubPlugin Release Package Requirements'

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.package_requirement.name} - {self.version}'


class SubPluginReleasePyPiRequirement(AbstractUUIDPrimaryKeyModel):
    """SubPlugin PyPi Requirement for Release model."""

    sub_plugin_release = models.ForeignKey(
        to='project_manager.SubPluginRelease',
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
            'The version of the PyPi package for this release of the sub_plugin.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('sub_plugin_release', 'pypi_requirement')
        verbose_name = 'SubPlugin Release PyPi Requirement'
        verbose_name_plural = 'SubPlugin Release PyPi Requirements'

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.pypi_requirement.name} - {self.version}'


class SubPluginReleaseVersionControlRequirement(AbstractUUIDPrimaryKeyModel):
    """SubPlugin VCS Requirement for Release model."""

    sub_plugin_release = models.ForeignKey(
        to='project_manager.SubPluginRelease',
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
            'The version of the VCS package for this release of the sub_plugin.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('sub_plugin_release', 'vcs_requirement')
        verbose_name = 'SubPlugin Release Version Control Requirement'
        verbose_name_plural = 'SubPlugin Release Version Control Requirements'

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.vcs_requirement.url} - {self.version}'
