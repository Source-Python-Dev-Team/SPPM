"""Factories for use when testing with Package functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.utils.timezone import get_current_timezone

# Third Party Django
import factory

# App
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageRelease,
    PackageReleaseDownloadRequirement,
    PackageReleasePackageRequirement,
    PackageReleasePyPiRequirement,
    PackageReleaseVersionControlRequirement,
    PackageTag,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageContributorFactory',
    'PackageFactory',
    'PackageGameFactory',
    'PackageReleaseFactory',
    'PackageReleaseDownloadRequirementFactory',
    'PackageReleasePackageRequirementFactory',
    'PackageReleasePyPiRequirementFactory',
    'PackageReleaseVersionControlRequirementFactory',
    'PackageTagFactory',
)


# =============================================================================
# FACTORIES
# =============================================================================
class PackageFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with Package objects."""

    name = factory.Sequence(function=lambda n: f'Package {n}')
    basename = factory.Sequence(function=lambda n: f'package_{n}')
    owner = factory.SubFactory(
        factory='test_utils.factories.users.ForumUserFactory',
    )
    created = factory.Faker('date_time', tzinfo=get_current_timezone())
    updated = factory.Faker('date_time', tzinfo=get_current_timezone())

    class Meta:
        """Define metaclass attributes."""

        model = Package


class PackageReleaseFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PackageRelease objects."""

    package = factory.SubFactory(
        factory='test_utils.factories.packages.PackageFactory',
    )
    version = factory.Sequence(function=lambda n: f'1.0.{n}')

    class Meta:
        """Define metaclass attributes."""

        model = PackageRelease


class PackageContributorFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PackageContributor objects."""

    package = factory.SubFactory(
        factory='test_utils.factories.packages.PackageFactory',
    )
    user = factory.SubFactory(
        factory='test_utils.factories.users.ForumUserFactory',
    )

    class Meta:
        """Define metaclass attributes."""

        model = PackageContributor


class PackageGameFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PackageGame objects."""

    package = factory.SubFactory(
        factory='test_utils.factories.packages.PackageFactory',
    )
    game = factory.SubFactory(
        factory='test_utils.factories.games.GameFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageGame


class PackageTagFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PackageTag objects."""

    package = factory.SubFactory(
        factory='test_utils.factories.packages.PackageFactory',
    )
    tag = factory.SubFactory(
        factory='test_utils.factories.tags.TagFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageTag


class PackageReleaseDownloadRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PackageReleaseDownloadRequirement objects."""

    package_release = factory.SubFactory(
        factory='test_utils.factories.packages.PackageReleaseFactory',
    )
    download_requirement = factory.SubFactory(
        factory='test_utils.factories.requirements.DownloadRequirement',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleaseDownloadRequirement


class PackageReleasePackageRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PackageReleasePackageRequirement objects."""

    package_release = factory.SubFactory(
        factory='test_utils.factories.packages.PackageReleaseFactory',
    )
    package_requirement = factory.SubFactory(
        factory='test_utils.factories.packages.PackageFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleasePackageRequirement


class PackageReleasePyPiRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PackageReleasePyPiRequirement objects."""

    package_release = factory.SubFactory(
        factory='test_utils.factories.packages.PackageReleaseFactory',
    )
    pypi_requirement = factory.SubFactory(
        factory='test_utils.factories.requirements.PyPiRequirement',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleasePyPiRequirement


class PackageReleaseVersionControlRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PackageReleaseVersionControlRequirement objects."""

    package_release = factory.SubFactory(
        factory='test_utils.factories.packages.PackageReleaseFactory',
    )
    vcs_requirement = factory.SubFactory(
        factory='test_utils.factories.requirements.VersionControlRequirementFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleaseVersionControlRequirement
