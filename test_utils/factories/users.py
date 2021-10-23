"""Factories for use when testing with User functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
import factory

# App
from users.models import ForumUser, User


# =============================================================================
# FACTORIES
# =============================================================================
class NonAdminUserFactory(factory.django.DjangoModelFactory):
    """Factory for a non-admin User to use in tests."""

    username = factory.Sequence(function=lambda n: f'user_{n}')
    is_staff = False
    is_superuser = False

    class Meta:
        """Define metaclass attributes."""

        model = User


class AdminUserFactory(NonAdminUserFactory):
    """Factory for an Admin User to use in tests."""

    is_staff = True
    is_superuser = True


class ForumUserFactory(factory.django.DjangoModelFactory):
    """Factory for Forum based User to use in tests."""

    user = factory.SubFactory(
        factory='test_utils.factories.users.NonAdminUserFactory',
    )
    forum_id = factory.Sequence(function=lambda n: n)

    class Meta:
        """Define metaclass attributes."""

        model = ForumUser
