"""SubPlugin model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.urls import reverse
from django.db import models

# App
from project_manager.common.constants import (
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
)
from project_manager.common.models import (
    ProjectBase,
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
from .abstract import SubPluginReleaseThroughBase, SubPluginThroughBase
from ..constants import SUB_PLUGIN_LOGO_URL
from ..helpers import (
    handle_sub_plugin_image_upload,
    handle_sub_plugin_logo_upload,
    handle_sub_plugin_zip_upload,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPlugin',
    'SubPluginContributor',
    'SubPluginGame',
    'SubPluginImage',
    'SubPluginRelease',
    'SubPluginTag',
)


# =============================================================================
# >> MODELS
# =============================================================================
class SubPlugin(ProjectBase):
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
    contributors = models.ManyToManyField(
        to='users.ForumUser',
        related_name='subplugin_contributions',
        through='sub_plugins.SubPluginContributor',
    )
    slug = models.SlugField(
        max_length=PROJECT_SLUG_MAX_LENGTH,
        blank=True,
    )
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='sub_plugins',
        on_delete=models.CASCADE,
    )
    supported_games = models.ManyToManyField(
        to='games.Game',
        related_name='subplugins',
        through='sub_plugins.SubPluginGame',
    )
    tags = models.ManyToManyField(
        to='tags.Tag',
        related_name='subplugins',
        through='sub_plugins.SubPluginTag',
    )

    handle_logo_upload = handle_sub_plugin_logo_upload
    logo_path = SUB_PLUGIN_LOGO_URL

    class Meta:
        verbose_name = 'SubPlugin'
        verbose_name_plural = 'SubPlugins'
        unique_together = (
            ('plugin', 'basename'),
            ('plugin', 'name'),
            ('plugin', 'slug'),
        )

    def __str__(self):
        """Return the string formatted name for the sub-plugin."""
        return f'{self.plugin.name}: {self.name}'

    def get_absolute_url(self):
        """Return the URL for the SubPlugin."""
        return reverse(
            viewname='plugins:sub-plugins:detail',
            kwargs={
                'slug': self.plugin.slug,
                'sub_plugin_slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
        """Set the id using the plugin's slug and the project's slug."""
        self.id = f'{self.plugin.slug}.{self.get_slug_value()}'
        super().save(*args, **kwargs)


class SubPluginRelease(ProjectRelease):
    """SubPlugin release type model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='releases',
        on_delete=models.CASCADE,
    )
    download_requirements = models.ManyToManyField(
        to='requirements.DownloadRequirement',
        related_name='required_in_sub_plugin_releases',
        through='sub_plugins.SubPluginReleaseDownloadRequirement',
    )
    package_requirements = models.ManyToManyField(
        to='packages.Package',
        related_name='required_in_sub_plugin_releases',
        through='sub_plugins.SubPluginReleasePackageRequirement',
    )
    pypi_requirements = models.ManyToManyField(
        to='requirements.PyPiRequirement',
        related_name='required_in_sub_plugin_releases',
        through='sub_plugins.SubPluginReleasePyPiRequirement',
    )
    vcs_requirements = models.ManyToManyField(
        to='requirements.VersionControlRequirement',
        related_name='required_in_sub_plugin_releases',
        through='sub_plugins.SubPluginReleaseVersionControlRequirement',
    )

    handle_zip_file_upload = handle_sub_plugin_zip_upload
    project_class = SubPlugin

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


class SubPluginImage(ProjectImage):
    """SubPlugin image type model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='images',
        on_delete=models.CASCADE,
    )

    handle_image_upload = handle_sub_plugin_image_upload


class SubPluginContributor(ProjectContributor, SubPluginThroughBase):
    """SubPlugin contributors through model."""

    class Meta:
        unique_together = ('sub_plugin', 'user')


class SubPluginGame(ProjectGame, SubPluginThroughBase):
    """SubPlugin supported_games through model."""

    class Meta:
        unique_together = ('sub_plugin', 'game')


class SubPluginTag(ProjectTag, SubPluginThroughBase):
    """SubPlugin tags through model."""

    class Meta:
        unique_together = ('sub_plugin', 'tag')


class SubPluginReleaseDownloadRequirement(
    ProjectReleaseDownloadRequirement, SubPluginReleaseThroughBase
):
    """"""

    class Meta:
        unique_together = ('sub_plugin_release', 'download_requirement')


class SubPluginReleasePackageRequirement(
    ProjectReleasePackageRequirement, SubPluginReleaseThroughBase
):
    """"""

    class Meta:
        unique_together = ('sub_plugin_release', 'package_requirement')


class SubPluginReleasePyPiRequirement(
    ProjectReleasePyPiRequirement, SubPluginReleaseThroughBase
):
    """"""

    class Meta:
        unique_together = ('sub_plugin_release', 'pypi_requirement')


class SubPluginReleaseVersionControlRequirement(
    ProjectReleaseVersionControlRequirement, SubPluginReleaseThroughBase
):
    """"""

    class Meta:
        unique_together = ('sub_plugin_release', 'vcs_requirement')
