"""Factories for use when testing with Plugin functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
# Third Party Django
import factory
from django.utils.timezone import get_current_timezone

# App
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginReleaseDownloadRequirement,
    PluginReleasePackageRequirement,
    PluginReleasePyPiRequirement,
    PluginReleaseVersionControlRequirement,
    PluginTag,
    SubPluginPath,
)

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "PluginContributorFactory",
    "PluginFactory",
    "PluginGameFactory",
    "PluginImageFactory",
    "PluginReleaseDownloadRequirementFactory",
    "PluginReleaseFactory",
    "PluginReleasePackageRequirementFactory",
    "PluginReleasePyPiRequirementFactory",
    "PluginReleaseVersionControlRequirementFactory",
    "PluginTagFactory",
    "SubPluginPathFactory",
)


# =============================================================================
# FACTORIES
# =============================================================================
class PluginFactory(factory.django.DjangoModelFactory):
    """Model factory for Plugin objects."""

    name = factory.Sequence(function=lambda n: f"Plugin {n}")
    basename = factory.Sequence(function=lambda n: f"plugin_{n}")
    owner = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )
    created = factory.Faker("date_time", tzinfo=get_current_timezone())
    updated = factory.Faker("date_time", tzinfo=get_current_timezone())

    class Meta:
        """Define metaclass attributes."""

        model = Plugin


class PluginReleaseFactory(factory.django.DjangoModelFactory):
    """Model factory for PluginRelease objects."""

    plugin = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginFactory",
    )
    version = factory.Sequence(function=lambda n: f"1.0.{n}")
    created_by = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )

    class Meta:
        """Define metaclass attributes."""

        model = PluginRelease


class PluginContributorFactory(factory.django.DjangoModelFactory):
    """Model factory for PluginContributor objects."""

    plugin = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginFactory",
    )
    user = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )

    class Meta:
        """Define metaclass attributes."""

        model = PluginContributor


class PluginGameFactory(factory.django.DjangoModelFactory):
    """Model factory for PluginGame objects."""

    plugin = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginFactory",
    )
    game = factory.SubFactory(
        factory="test_utils.factories.games.GameFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginGame


class PluginImageFactory(factory.django.DjangoModelFactory):
    """Model factory for PluginImage objects."""

    plugin = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginFactory",
    )
    image = factory.Sequence(function=lambda n: f"image_{n}.jpg")

    class Meta:
        """Define the metaclass attributes."""

        model = PluginImage


class PluginTagFactory(factory.django.DjangoModelFactory):
    """Model factory for PluginTag objects."""

    plugin = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginFactory",
    )
    tag = factory.SubFactory(
        factory="test_utils.factories.tags.TagFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginTag


class PluginReleaseDownloadRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PluginReleaseDownloadRequirement objects."""

    plugin_release = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginReleaseFactory",
    )
    download_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.DownloadRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleaseDownloadRequirement


class PluginReleasePackageRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PluginReleasePackageRequirement objects."""

    plugin_release = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginReleaseFactory",
    )
    package_requirement = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleasePackageRequirement


class PluginReleasePyPiRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PluginReleasePyPiRequirement objects."""

    plugin_release = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginReleaseFactory",
    )
    pypi_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.PyPiRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleasePyPiRequirement


class PluginReleaseVersionControlRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for PluginReleaseVersionControlRequirement objects."""

    plugin_release = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginReleaseFactory",
    )
    vcs_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.VersionControlRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleaseVersionControlRequirement


class SubPluginPathFactory(factory.django.DjangoModelFactory):
    """Model factory for SubPluginPath objects."""

    plugin = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginFactory",
    )
    path = factory.Sequence(function=lambda n: f"some/path/{n}")

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginPath
