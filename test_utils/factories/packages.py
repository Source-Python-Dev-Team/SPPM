"""Factories for use when testing with Package functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
# Third Party Django
import factory
from django.utils.timezone import get_current_timezone

# App
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
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
    "PackageContributorFactory",
    "PackageFactory",
    "PackageGameFactory",
    "PackageImageFactory",
    "PackageReleaseDownloadRequirementFactory",
    "PackageReleaseFactory",
    "PackageReleasePackageRequirementFactory",
    "PackageReleasePyPiRequirementFactory",
    "PackageReleaseVersionControlRequirementFactory",
    "PackageTagFactory",
)


# =============================================================================
# FACTORIES
# =============================================================================
class PackageFactory(factory.django.DjangoModelFactory):
    """Model factory for Package objects."""

    name = factory.Sequence(function=lambda n: f"Package {n}")
    basename = factory.Sequence(function=lambda n: f"package_{n}")
    owner = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )
    created = factory.Faker("date_time", tzinfo=get_current_timezone())
    updated = factory.Faker("date_time", tzinfo=get_current_timezone())

    class Meta:
        """Define metaclass attributes."""

        model = Package


class PackageReleaseFactory(factory.django.DjangoModelFactory):
    """Model factory for PackageRelease objects."""

    package = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )
    version = factory.Sequence(function=lambda n: f"1.0.{n}")
    created_by = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )

    class Meta:
        """Define metaclass attributes."""

        model = PackageRelease


class PackageContributorFactory(factory.django.DjangoModelFactory):
    """Model factory for PackageContributor objects."""

    package = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )
    user = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )

    class Meta:
        """Define metaclass attributes."""

        model = PackageContributor


class PackageGameFactory(factory.django.DjangoModelFactory):
    """Model factory for PackageGame objects."""

    package = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )
    game = factory.SubFactory(
        factory="test_utils.factories.games.GameFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageGame


class PackageImageFactory(factory.django.DjangoModelFactory):
    """Model factory for PackageImage objects."""

    package = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )
    image = factory.Sequence(function=lambda n: f"image_{n}.jpg")

    class Meta:
        """Define the metaclass attributes."""

        model = PackageImage


class PackageTagFactory(factory.django.DjangoModelFactory):
    """Model factory for PackageTag objects."""

    package = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )
    tag = factory.SubFactory(
        factory="test_utils.factories.tags.TagFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageTag


class PackageReleaseDownloadRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PackageReleaseDownloadRequirement objects."""

    package_release = factory.SubFactory(
        factory="test_utils.factories.packages.PackageReleaseFactory",
    )
    download_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.DownloadRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleaseDownloadRequirement


class PackageReleasePackageRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PackageReleasePackageRequirement objects."""

    package_release = factory.SubFactory(
        factory="test_utils.factories.packages.PackageReleaseFactory",
    )
    package_requirement = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleasePackageRequirement


class PackageReleasePyPiRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PackageReleasePyPiRequirement objects."""

    package_release = factory.SubFactory(
        factory="test_utils.factories.packages.PackageReleaseFactory",
    )
    pypi_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.PyPiRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleasePyPiRequirement


class PackageReleaseVersionControlRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PackageReleaseVersionControlRequirement objects."""

    package_release = factory.SubFactory(
        factory="test_utils.factories.packages.PackageReleaseFactory",
    )
    vcs_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.VersionControlRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PackageReleaseVersionControlRequirement
