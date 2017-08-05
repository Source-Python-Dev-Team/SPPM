# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# App
from project_manager.common.models import ProjectBase, ReleaseBase
from project_manager.common.validators import basename_validator
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
class Package(ProjectBase):
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
        primary_key=True,
    )

    handle_logo_upload = handle_package_logo_upload

    def get_absolute_url(self):
        return reverse(
            viewname='packages:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
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

        super().save(*args, **kwargs)


class PackageRelease(ReleaseBase):
    """Store the information for """
    package = models.ForeignKey(
        to='packages.Package',
        related_name='releases',
    )

    handle_zip_file_upload = handle_package_zip_upload

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
