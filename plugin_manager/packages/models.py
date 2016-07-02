# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# 3rd-Party
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
from .constants import PACKAGE_LOGO_URL, PACKAGE_RELEASE_URL
from .helpers import handle_package_image_upload
from .helpers import handle_package_logo_upload
from .helpers import handle_package_zip_upload
from ..common.models import CommonBase, DownloadStatistics
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OldPackageRelease',
    'Package',
    'PackageImage',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class Package(CommonBase):
    owner = models.ForeignKey(
        to='plugin_manager.ForumUser',
        related_name='packages',
    )
    contributors = models.ManyToManyField(
        to='plugin_manager.ForumUser',
        related_name='package_contributions',
    )
    package_requirements = models.ManyToManyField(
        to='plugin_manager.Package',
        related_name='required_in_packages',
    )
    pypi_requirements = models.ManyToManyField(
        to='plugin_manager.PyPiRequirement',
        related_name='required_in_packages',
    )
    zip_file = models.FileField(
        upload_to=handle_package_zip_upload,
    )
    logo = models.ImageField(
        upload_to=handle_package_logo_upload,
        blank=True,
        null=True,
    )
    supported_games = models.ManyToManyField(
        to='plugin_manager.Game',
        related_name='packages',
    )

    field_tracker = FieldTracker(['version', 'version_notes', 'zip_file'])

    def get_absolute_url(self):
        return reverse(
            viewname='packages:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Remove the old logo before storing the new one."""
        if self.logo and PACKAGE_LOGO_URL not in str(self.logo):
            path = Path(settings.MEDIA_ROOT) / PACKAGE_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.basename]
                if logo:
                    logo[0].remove()

        tracker = self.field_tracker
        release = None
        version = tracker.saved_data.get('version', None)
        if tracker.has_changed('version') and version:
            release = OldPackageRelease(
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

        super(Package, self).save(
            force_insert, force_update, using, update_fields)

        if release is not None:
            release.save()
            self.previous_releases.add(release)


class OldPackageRelease(models.Model):
    """Store the information for """
    version = models.CharField(
        max_length=8,
    )
    version_notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
    )
    zip_file = models.FileField()
    package = models.ForeignKey(
        to='plugin_manager.Package',
        related_name='previous_releases',
    )

    class Meta:
        verbose_name = 'Old Release (Package)'
        verbose_name_plural = 'Old Releases (Package)'


class PackageImage(models.Model):
    image = models.ImageField(
        upload_to=handle_package_image_upload,
    )
    package = models.ForeignKey(
        to='plugin_manager.Package',
        related_name='images',
    )

    class Meta:
        verbose_name = 'Image (Package)'
        verbose_name_plural = 'Images (Package)'


class PackageDownloadStatistics(DownloadStatistics):

    @property
    def full_url(self):
        return PACKAGE_RELEASE_URL + self.download_url
