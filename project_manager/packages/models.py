# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# 3rd-Party Django
from precise_bbcode.fields import BBCodeTextField

# App
from project_manager.common.models import CommonBase, Release
from project_manager.common.validators import (
    basename_validator, version_validator,
)
from project_manager.users.models import ForumUser
from .constants import PACKAGE_LOGO_URL
from .helpers import handle_package_image_upload
from .helpers import handle_package_logo_upload
from .helpers import handle_package_zip_upload


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageRelease',
    'Package',
    'PackageImage',
)


# =============================================================================
# >> MODELS
# =============================================================================
class Package(CommonBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        help_text=(
            "The name of the package. Do not include the version, as that is "
            "added dynamically to the package's page."
        ),
    )
    basename = models.CharField(
        max_length=32,
        validators=[basename_validator],
        unique=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        blank=True,
    )
    logo = models.ImageField(
        upload_to=handle_package_logo_upload,
        blank=True,
        null=True,
        help_text="The package's logo image.",
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
            path = settings.MEDIA_ROOT / PACKAGE_LOGO_URL
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
        to='packages.Package',
        related_name='releases',
    )
    version = models.CharField(
        max_length=8,
        validators=[version_validator],
        help_text='The version for this release of the package.',
    )
    notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
        help_text='The notes for this particular release of the package.',
    )
    zip_file = models.FileField(
        upload_to=handle_package_zip_upload,
    )

    class Meta:
        verbose_name = 'Release'
        verbose_name_plural = 'Releases'

    def get_absolute_url(self):
        return reverse(
            viewname='package-download',
            kwargs={
                'slug': self.package.slug,
                'zip_file': self.file_name,
            }
        )


class PackageImage(models.Model):
    image = models.ImageField(
        upload_to=handle_package_image_upload,
    )
    package = models.ForeignKey(
        to='packages.Package',
        related_name='images',
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
