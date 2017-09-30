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
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        max_length=256,
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
