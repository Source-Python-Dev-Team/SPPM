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

# App
from .constants import PACKAGE_LOGO_URL
from .helpers import handle_package_image_upload
from .helpers import handle_package_logo_upload
from .helpers import handle_package_zip_upload
from ..common.models import CommonBase, Release
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageRelease',
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
    logo = models.ImageField(
        upload_to=handle_package_logo_upload,
        blank=True,
        null=True,
    )
    supported_games = models.ManyToManyField(
        to='plugin_manager.Game',
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
        if self.logo and PACKAGE_LOGO_URL not in str(self.logo):
            path = Path(settings.MEDIA_ROOT) / PACKAGE_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.slug]
                if logo:
                    logo[0].remove()

        # TODO: Set the owner based on the user that is logged in
        if not self.owner_id:
            from random import choice
            self.owner = choice(ForumUser.objects.all())

        super(Package, self).save(
            force_insert, force_update, using, update_fields)


class PackageRelease(Release):
    """Store the information for """
    package = models.ForeignKey(
        to='plugin_manager.Package',
        related_name='releases',
    )
    zip_file = models.FileField(
        upload_to=handle_package_zip_upload,
    )

    class Meta:
        verbose_name = 'Release (Package)'
        verbose_name_plural = 'Releases (Package)'


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
