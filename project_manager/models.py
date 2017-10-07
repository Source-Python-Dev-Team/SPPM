"""Base app models."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.db import models

# App
from .constants import USER_EMAIL_MAX_LENGTH, USER_USERNAME_MAX_LENGTH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'User',
)


# =============================================================================
# >> MODELS
# =============================================================================
class User(AbstractBaseUser, PermissionsMixin):
    """Base User Model."""

    username = models.CharField(
        max_length=USER_USERNAME_MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        max_length=USER_EMAIL_MAX_LENGTH,
        blank=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def get_full_name(self):
        """Return the full name for the user."""
        return self.username
