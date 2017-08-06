"""Tag model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import models

# App
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
        max_length=16,
        unique=True,
        validators=[tag_name_validator],
    )

    def __str__(self):
        return self.name
