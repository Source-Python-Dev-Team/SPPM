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
# >> MODELS
# =============================================================================
class User(AbstractBaseUser, PermissionsMixin):
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
        """Returns the short name for the user."""
        return self.username
