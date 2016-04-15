# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

# App Imports
from .constants import FORUM_MEMBER_URL


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'User',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class User(models.Model):
    name = models.CharField(
        max_length=30,
    )
    forum_id = models.IntegerField(
        primary_key=True,
        unique=True,
    )

    def get_absolute_url(self):
        return reverse(
            viewname='users:user_detail',
            kwargs={
                'pk': self.forum_id,
            }
        )

    def get_forum_url(self):
        return FORUM_MEMBER_URL.format(self.forum_id)
