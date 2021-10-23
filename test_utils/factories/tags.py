"""Factories for use when testing with Game functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
import factory

# App
from tags.models import Tag


# =============================================================================
# FACTORIES
# =============================================================================
class TagFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with Game objects."""

    name = factory.Sequence(function=lambda n: f'tag_{n}')
    creator = factory.SubFactory(
        factory='test_utils.factories.users.ForumUserFactory',
    )

    class Meta:
        """Define metaclass attributes."""

        model = Tag
