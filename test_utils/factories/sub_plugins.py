"""Factories for use when testing with SubPlugin functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
# Third Party Django
import factory
from django.utils.timezone import get_current_timezone

# App
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
    SubPluginTag,
)

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "SubPluginContributorFactory",
    "SubPluginFactory",
    "SubPluginGameFactory",
    "SubPluginImageFactory",
    "SubPluginReleaseDownloadRequirementFactory",
    "SubPluginReleaseFactory",
    "SubPluginReleasePackageRequirementFactory",
    "SubPluginReleasePyPiRequirementFactory",
    "SubPluginReleaseVersionControlRequirementFactory",
    "SubPluginTagFactory",
)


# =============================================================================
# FACTORIES
# =============================================================================
class SubPluginFactory(factory.django.DjangoModelFactory):
    """Model factory for SubPlugin objects."""

    plugin = factory.SubFactory(
        factory="test_utils.factories.plugins.PluginFactory",
    )
    name = factory.Sequence(function=lambda n: f"SubPlugin {n}")
    basename = factory.Sequence(function=lambda n: f"sub_plugin_{n}")
    owner = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )
    created = factory.Faker("date_time", tzinfo=get_current_timezone())
    updated = factory.Faker("date_time", tzinfo=get_current_timezone())

    class Meta:
        """Define metaclass attributes."""

        model = SubPlugin


class SubPluginReleaseFactory(factory.django.DjangoModelFactory):
    """Model factory for SubPluginRelease objects."""

    sub_plugin = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginFactory",
    )
    version = factory.Sequence(function=lambda n: f"1.0.{n}")
    created_by = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )

    class Meta:
        """Define metaclass attributes."""

        model = SubPluginRelease


class SubPluginContributorFactory(factory.django.DjangoModelFactory):
    """Model factory for SubPluginContributor objects."""

    sub_plugin = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginFactory",
    )
    user = factory.SubFactory(
        factory="test_utils.factories.users.ForumUserFactory",
    )

    class Meta:
        """Define metaclass attributes."""

        model = SubPluginContributor


class SubPluginGameFactory(factory.django.DjangoModelFactory):
    """Model factory for SubPluginGame objects."""

    sub_plugin = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginFactory",
    )
    game = factory.SubFactory(
        factory="test_utils.factories.games.GameFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginGame


class SubPluginImageFactory(factory.django.DjangoModelFactory):
    """Model factory for SubPluginImage objects."""

    sub_plugin = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginFactory",
    )
    image = factory.Sequence(function=lambda n: f"image_{n}.jpg")

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginImage


class SubPluginTagFactory(factory.django.DjangoModelFactory):
    """Model factory for SubPluginTag objects."""

    sub_plugin = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginFactory",
    )
    tag = factory.SubFactory(
        factory="test_utils.factories.tags.TagFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginTag


class SubPluginReleaseDownloadRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for SubPluginReleaseDownloadRequirement objects."""

    sub_plugin_release = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginReleaseFactory",
    )
    download_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.DownloadRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginReleaseDownloadRequirement


class SubPluginReleasePackageRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for SubPluginReleasePackageRequirement objects."""

    sub_plugin_release = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginReleaseFactory",
    )
    package_requirement = factory.SubFactory(
        factory="test_utils.factories.packages.PackageFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginReleasePackageRequirement


class SubPluginReleasePyPiRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for SubPluginReleasePyPiRequirement objects."""

    sub_plugin_release = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginReleaseFactory",
    )
    pypi_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.PyPiRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginReleasePyPiRequirement


class SubPluginReleaseVersionControlRequirementFactory(
    factory.django.DjangoModelFactory,
):
    """Model factory for SubPluginReleaseVersionControlRequirement objects."""

    sub_plugin_release = factory.SubFactory(
        factory="test_utils.factories.sub_plugins.SubPluginReleaseFactory",
    )
    vcs_requirement = factory.SubFactory(
        factory="test_utils.factories.requirements.VersionControlRequirementFactory",
    )

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginReleaseVersionControlRequirement
