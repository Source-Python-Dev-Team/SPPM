"""Tag model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import models

# App
from .constants import TAG_NAME_MAX_LENGTH
from .validators import tag_name_validator


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'Tag',
)


# =============================================================================
# >> MODELS
# =============================================================================
class Tag(models.Model):
    """Model used to store tags for projects."""

    name = models.CharField(
        max_length=TAG_NAME_MAX_LENGTH,
        primary_key=True,
        unique=True,
        validators=[tag_name_validator],
    )
    black_listed = models.BooleanField(
        default=False,
    )

    def __str__(self):
        """Return the tag's name."""
        return self.name
