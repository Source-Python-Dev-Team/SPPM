"""User model classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.conf import settings
from django.urls import reverse
from django.db import models

# App
from users.constants import (
    FORUM_MEMBER_URL,
    USER_USERNAME_MAX_LENGTH,
)
from users.models.managers import UserManager


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUser',
    'User',
)


# =============================================================================
# MODELS
# =============================================================================
class User(AbstractBaseUser, PermissionsMixin):
    """Base User Model."""

    username = models.CharField(
        editable=False,
        max_length=USER_USERNAME_MAX_LENGTH,
        unique=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def get_full_name(self):
        """Return the full name for the user."""
        return self.username


class ForumUser(models.Model):
    """Model for User based information."""

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        related_name='forum_user',
        on_delete=models.CASCADE,
    )
    forum_id = models.IntegerField(
        primary_key=True,
        unique=True,
    )

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'Forum User'
        verbose_name_plural = 'Forum Users'

    def __str__(self):
        """Return the ForumUser's username."""
        return self.user.username

    def get_absolute_url(self):
        """Return the URL for the user."""
        return reverse(
            viewname='users:detail',
            kwargs={
                'pk': self.forum_id,
            }
        )

    def get_forum_url(self):
        """Return the user's forum URL."""
        return FORUM_MEMBER_URL.format(user_id=self.forum_id)
