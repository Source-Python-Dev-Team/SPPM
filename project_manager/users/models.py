"""User model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
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
    """Model for User based information."""

    username = models.CharField(
        max_length=30,
        unique=True,
    )
    id = models.IntegerField(
        primary_key=True,
        unique=True,
    )

    class Meta:
        verbose_name = 'Forum User'
        verbose_name_plural = 'Forum Users'

    def __str__(self):
        """Return the ForumUser's username."""
        return self.username

    def get_absolute_url(self):
        """Return the URL for the user."""
        return reverse(
            viewname='users:detail',
            kwargs={
                'pk': self.id,
            }
        )

    def get_forum_url(self):
        """Return the user's forum URL."""
        return FORUM_MEMBER_URL.format(user_id=self.id)
