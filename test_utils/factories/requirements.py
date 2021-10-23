"""Factories for use when testing with Game functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
import factory

# App
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadRequirementFactory',
    'PyPiRequirementFactory',
    'VersionControlRequirementFactory',
)


# =============================================================================
# FACTORIES
# =============================================================================
class DownloadRequirementFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with Download Requirement objects."""

    url = factory.Sequence(function=lambda n: f'download_{n}')

    class Meta:
        """Define metaclass attributes."""

        model = DownloadRequirement


class PyPiRequirementFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PyPi Requirement objects."""

    name = factory.Sequence(function=lambda n: f'pypi_{n}')

    class Meta:
        """Define metaclass attributes."""

        model = PyPiRequirement


class VersionControlRequirementFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with VCS Requirement objects."""

    url = factory.Sequence(function=lambda n: f'vcs_{n}')

    class Meta:
        """Define metaclass attributes."""

        model = VersionControlRequirement
