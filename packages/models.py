# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# 3rd-Party Python
from path import Path

# Django Imports
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now

# 3rd-Party Django Imports
from precise_bbcode.fields import BBCodeTextField

# Project Imports
from common.models import CommonBase

# App Imports
from .helpers import handle_package_image_upload
from .helpers import handle_package_logo_upload
from .helpers import handle_package_zip_upload


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
        to='users.ForumUser',
        related_name='packages',
    )
    contributors = models.ManyToManyField(
        to='users.ForumUser',
        related_name='package_contributions',
    )
    package_requirements = models.ManyToManyField(
        to='packages.Package',
        related_name='required_in_packages',
    )
    pypi_requirements = models.ManyToManyField(
        to='pypi.PyPiRequirement',
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
        to='games.Game',
        related_name='packages',
    )

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
        if self.logo and u'logo/' not in self.logo:
            path = Path(settings.MEDIA_ROOT) / 'logos' / 'package'
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.basename]
                if logo:
                    logo[0].remove()

        release = None

        if self.current_version and self.current_version != self.version:
            release = OldPackageRelease(
                version=self.current_version,
                version_notes=self.current_version_notes,
                zip_file=self.current_zip_file,
                package=self,
            )
            self.date_last_updated = now()

        self.current_version = self.version
        self.current_version_notes = self.version_notes
        self.current_zip_file = self.zip_file

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
        to='packages.Package',
        related_name='previous_releases',
    )


class PackageImage(models.Model):
    image = models.ImageField(
        upload_to=handle_package_image_upload,
    )
    package = models.ForeignKey(
        to='packages.Package',
        related_name='images',
    )
