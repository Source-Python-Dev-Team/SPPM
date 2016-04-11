from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from common.models import CommonBase, readable_data_file_types

from .helpers import handle_package_upload


__all__ = (
    'OldPackageRelease',
    'Package',
)


# Create your models here.
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
        upload_to=handle_package_upload,
    )

    allowed_file_types = dict(CommonBase.allowed_file_types)
    allowed_file_types.update({
        'addons/source-python/packages/custom/': [
            'py',
        ] + readable_data_file_types,
    })

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
    zip_file = models.FileField()
    version_notes = models.TextField(
        max_length=512,
        blank=True,
        null=True,
    )
    package = models.ForeignKey(
        to='packages.Package',
        related_name='previous_releases',
    )
