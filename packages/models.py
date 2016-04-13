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
class OldPackageRelease(models.Model):
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


class Package(CommonBase):
    user = models.ForeignKey(
        to='users.User',
        related_name='packages',
    )
    contributors = models.ManyToManyField(
        to='users.User',
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

    old_release_class = OldPackageRelease

    def get_absolute_url(self):
        return reverse(
            viewname='packages:package_detail',
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

        super(Package, self).save(
            force_insert, force_update, using, update_fields)


class PackageImage(models.Model):
    image = models.ImageField(
        upload_to=handle_package_image_upload,
    )
    package = models.ForeignKey(
        to='packages.Package',
        related_name='images',
    )
