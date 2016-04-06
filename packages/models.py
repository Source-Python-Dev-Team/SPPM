from __future__ import unicode_literals

from common.models import CommonBase, readable_data_file_types

from django.db import models


__all__ = (
    'Package',
)


# Create your models here.
class Package(CommonBase):
    """"""

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

    allowed_file_types = dict(CommonBase.allowed_file_types)
    allowed_file_types.update({
        'addons/source-python/packages/custom/': [
            'py',
        ] + readable_data_file_types,
    })

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
