# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# 3rd-Party Python
from path import Path

# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now

# 3rd-Party Django
from model_utils import FieldTracker
from precise_bbcode.fields import BBCodeTextField

# App
from .constants import PLUGIN_LOGO_URL, PLUGIN_RELEASE_URL
from .helpers import handle_plugin_image_upload
from .helpers import handle_plugin_logo_upload
from .helpers import handle_plugin_zip_upload
from ..common.models import CommonBase, DownloadStatistics
from ..common.validators import sub_plugin_path_validator
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OldPluginRelease',
    'Plugin',
    'PluginDownloadStatistics',
    'PluginImage',
    'SubPluginPath',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class Plugin(CommonBase):
    owner = models.ForeignKey(
        to='plugin_manager.ForumUser',
        related_name='plugins',
    )
    contributors = models.ManyToManyField(
        to='plugin_manager.ForumUser',
        related_name='plugin_contributions',
    )
    package_requirements = models.ManyToManyField(
        to='plugin_manager.Package',
        related_name='required_in_plugins',
    )
    pypi_requirements = models.ManyToManyField(
        to='plugin_manager.PyPiRequirement',
        related_name='required_in_plugins',
    )
    zip_file = models.FileField(
        upload_to=handle_plugin_zip_upload,
    )
    logo = models.ImageField(
        upload_to=handle_plugin_logo_upload,
        blank=True,
        null=True,
    )
    supported_games = models.ManyToManyField(
        to='plugin_manager.Game',
        related_name='plugins',
    )

    field_tracker = FieldTracker(['version', 'version_notes', 'zip_file'])

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Remove the old logo before storing the new one."""
        if self.logo and PLUGIN_LOGO_URL not in str(self.logo):
            path = Path(settings.MEDIA_ROOT) / PLUGIN_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.basename]
                if logo:
                    logo[0].remove()

        tracker = self.field_tracker
        release = None
        version = tracker.saved_data.get('version', None)
        if tracker.has_changed('version') and version:
            release = OldPluginRelease(
                version=version,
                version_notes=tracker.saved_data['version_notes'],
                zip_file=tracker.saved_data['zip_file'],
                plugin=self,
            )
            self.date_last_updated = now()

        # TODO: Set the owner based on the user that is logged in
        if not self.owner_id:
            from random import choice
            self.owner = choice(ForumUser.objects.all())

        super(Plugin, self).save(
            force_insert, force_update, using, update_fields)

        if release is not None:
            release.save()
            self.previous_releases.add(release)


class OldPluginRelease(models.Model):
    version = models.CharField(
        max_length=8,
    )
    version_notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
    )
    zip_file = models.FileField()
    plugin = models.ForeignKey(
        to='plugin_manager.Plugin',
        related_name='previous_releases',
    )

    class Meta:
        verbose_name = 'Old Release (Plugin)'
        verbose_name_plural = 'Old Releases (Plugin)'


class SubPluginPath(models.Model):
    plugin = models.ForeignKey(
        to='plugin_manager.Plugin',
        related_name='paths',
    )
    path = models.CharField(
        max_length=256,
        validators=[sub_plugin_path_validator],
    )

    class Meta:
        verbose_name = 'SubPlugin path (Plugin)'
        verbose_name_plural = 'SubPlugin paths (Plugin)'


class PluginImage(models.Model):
    image = models.ImageField(
        upload_to=handle_plugin_image_upload,
    )
    plugin = models.ForeignKey(
        to='plugin_manager.Plugin',
        related_name='images',
    )

    class Meta:
        verbose_name = 'Image (Plugin)'
        verbose_name_plural = 'Images (Plugin)'


class PluginDownloadStatistics(DownloadStatistics):

    @property
    def full_url(self):
        return PLUGIN_RELEASE_URL + self.download_url
