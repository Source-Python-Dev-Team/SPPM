"""User model managers."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManger


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'UserManager',
)


# =============================================================================
# MODEL MANAGERS
# =============================================================================
class UserManager(DjangoUserManger):
    """User model manager."""

    def _create_user(self, username, email, password, **extra_fields):
        """Overwrite method to not use email."""
        if not username:
            raise ValueError("The given username must be set")

        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        meta_class = getattr(self.model, '_meta')
        username = apps.get_model(
            app_label=meta_class.app_label,
            model_name=meta_class.object_name,
        ).normalize_username(
            username=username,
        )
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
