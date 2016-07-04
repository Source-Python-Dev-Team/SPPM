# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# Django
from django.core.urlresolvers import reverse
from django.db import models

# App
from .constants import FORUM_MEMBER_URL


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUser',
)


# =============================================================================
# >> MODELS
# =============================================================================
class ForumUser(models.Model):
    username = models.CharField(
        max_length=30,
        unique=True,
    )
    id = models.IntegerField(
        primary_key=True,
        unique=True,
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse(
            viewname='users:detail',
            kwargs={
                'pk': self.id,
            }
        )

    def get_forum_url(self):
        return FORUM_MEMBER_URL.format(user_id=self.id)
