# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

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
    name = models.CharField(
        max_length=16,
        unique=True,
        validators=[tag_name_validator],
    )

    def __str__(self):
        return self.name
