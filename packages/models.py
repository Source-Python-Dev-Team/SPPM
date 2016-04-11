# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.core.urlresolvers import reverse
from django.db import models

# 3rd-Party Django Imports
from precise_bbcode.fields import BBCodeTextField

# Project Imports
from common.models import CommonBase

# App Imports
from .helpers import handle_package_logo_upload
from .helpers import handle_package_zip_upload


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OldPackageRelease',
    'Package',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
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
        if self.current_version and self.current_zip_file:
            release = OldPackageRelease(
                version=self.current_version,
                version_notes=self.current_version_notes,
                zip_file=self.current_zip_file,
            )
            release.save()
            self.previous_releases.add(release)
        self.current_version = self.version
        self.current_version_notes = self.version_notes
        self.current_zip_file = self.zip_file
        super(Package, self).save(
            force_insert, force_update, using, update_fields
        )


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
