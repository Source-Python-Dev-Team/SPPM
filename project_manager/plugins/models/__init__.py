"""Plugin model classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models

# App
from project_manager.common.constants import (
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
)
from project_manager.common.models import (
    Project,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectReleaseDownloadRequirement,
    ProjectReleasePackageRequirement,
    ProjectReleasePyPiRequirement,
    ProjectReleaseVersionControlRequirement,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from project_manager.common.models import AbstractUUIDPrimaryKeyModel
from project_manager.plugins.constants import PLUGIN_LOGO_URL, PATH_MAX_LENGTH
from project_manager.plugins.helpers import (
    handle_plugin_image_upload,
    handle_plugin_logo_upload,
    handle_plugin_zip_upload,
)
from project_manager.plugins.models.abstract import (
    PluginReleaseThroughBase,
    PluginThroughBase,
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

    @property
    def project(self):
        """Return the Plugin."""
        return self.plugin

    class Meta(ProjectRelease.Meta):
        """Define metaclass attributes."""

        unique_together = ('plugin', 'version')

    def get_absolute_url(self):
        """Return the URL for the PluginRelease."""
        return reverse(
            viewname='plugin-download',
            kwargs={
                'slug': self.plugin.slug,
                'zip_file': self.file_name,
            }
        )


class PluginImage(ProjectImage):
    """Plugin image type model."""

    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        related_name='images',
        on_delete=models.CASCADE,
    )

    handle_image_upload = handle_plugin_image_upload


class PluginContributor(PluginThroughBase, ProjectContributor):
    """Plugin contributors through model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin', 'user')


class PluginGame(ProjectGame, PluginThroughBase):
    """Plugin supported_games through model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin', 'game')


class PluginTag(ProjectTag, PluginThroughBase):
    """Plugin tags through model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin', 'tag')


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

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'SubPlugin Path'
        verbose_name_plural = 'SubPlugin Paths'
        unique_together = ('path', 'plugin')

    def __str__(self):
        """Return the path."""
        return str(self.path)

    def clean(self):
        """Validate that at least one of the Allow fields is True."""
        if not any([
            self.allow_module,
            self.allow_package_using_basename,
            self.allow_package_using_init,
        ]):
            message = 'At least one of the "Allow" fields must be True.'
            raise ValidationError({
                'allow_module': message,
                'allow_package_using_basename': message,
                'allow_package_using_init': message,
            })
        return super().clean()

    def get_absolute_url(self):
        """Return the SubPluginPath listing URL for the Plugin."""
        return reverse(
            viewname='plugins:path_list',
            kwargs={
                'slug': self.plugin.slug,
            }
        )


class PluginReleaseDownloadRequirement(
    ProjectReleaseDownloadRequirement, PluginReleaseThroughBase
):
    """Plugin Download Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'download_requirement')


class PluginReleasePackageRequirement(
    ProjectReleasePackageRequirement, PluginReleaseThroughBase
):
    """Plugin Package Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'package_requirement')


class PluginReleasePyPiRequirement(
    ProjectReleasePyPiRequirement, PluginReleaseThroughBase
):
    """Plugin PyPi Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'pypi_requirement')


class PluginReleaseVersionControlRequirement(
    ProjectReleaseVersionControlRequirement, PluginReleaseThroughBase
):
    """Plugin VCS Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('plugin_release', 'vcs_requirement')
