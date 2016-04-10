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
            viewname='packages:package-detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_basename(self, zip_file):
        basename = None
        for x in zip_file.filelist:
            if x.filename.startswith('addons/source-python/packages/custom/'):
                current = x.filename.split(
                    'addons/source-python/packages/custom/', 1)[1]
                if not current:
                    continue
                if not current.endswith('.py'):
                    continue
                current = current.split('/', 1)[0]
                if current.endswith('.py'):
                    current = current.rsplit('.', 1)[0]
                if basename is None:
                    basename = current
                elif basename != current:
                    raise ValueError('Multiple packages included in zip.')
        if basename is None:
            raise ValueError('No package found in zip.')
        return basename

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        if self.current_version and self.current_zip_file:
            release = OldPackageRelease(
                version=self.current_version,
                zip_file=self.current_zip_file,
            )
            release.save()
            self.previous_releases.add(release)
        self.current_version = self.version
        self.current_zip_file = self.zip_file
        super(Package, self).save(
            force_insert, force_update, using, update_fields
        )


class OldPackageRelease(models.Model):
    version = models.CharField(
        max_length=8,
    )
    zip_file = models.FileField()
    package = models.ForeignKey(
        to='packages.Package',
        related_name='previous_releases',
    )
