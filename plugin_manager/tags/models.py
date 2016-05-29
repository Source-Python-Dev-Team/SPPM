# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# Django
from django.db import models


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'Tag',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class Tag(models.Model):
    name = models.CharField(
        max_length=16,
        unique=True,
    )

    def __str__(self):
        return self.name
