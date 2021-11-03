"""Factories for use when testing with Plugin functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.utils.timezone import get_current_timezone

# Third Party Django
import factory

# App
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
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
    'PluginContributorFactory',
    'PluginFactory',
    'PluginGameFactory',
    'PluginReleaseFactory',
    'PluginReleaseDownloadRequirementFactory',
    'PluginReleasePackageRequirementFactory',
    'PluginReleasePyPiRequirementFactory',
    'PluginReleaseVersionControlRequirementFactory',
    'PluginTagFactory',
    'SubPluginPathFactory',
)


# =============================================================================
# FACTORIES
# =============================================================================
class PluginFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with Plugin objects."""

    name = factory.Sequence(function=lambda n: f'Plugin {n}')
    basename = factory.Sequence(function=lambda n: f'plugin_{n}')
    owner = factory.SubFactory(
        factory='test_utils.factories.users.ForumUserFactory',
    )
    created = factory.Faker('date_time', tzinfo=get_current_timezone())
    updated = factory.Faker('date_time', tzinfo=get_current_timezone())

    class Meta:
        """Define metaclass attributes."""

        model = Plugin


class PluginReleaseFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PluginRelease objects."""

    plugin = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginFactory',
    )
    version = factory.Sequence(function=lambda n: f'1.0.{n}')

    class Meta:
        """Define metaclass attributes."""

        model = PluginRelease


class PluginContributorFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PluginContributor objects."""

    plugin = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginFactory',
    )
    user = factory.SubFactory(
        factory='test_utils.factories.users.ForumUserFactory',
    )

    class Meta:
        """Define metaclass attributes."""

        model = PluginContributor


class PluginGameFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PluginGame objects."""

    plugin = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginFactory',
    )
    game = factory.SubFactory(
        factory='test_utils.factories.games.GameFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginGame


class PluginTagFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with PluginTag objects."""

    plugin = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginFactory',
    )
    tag = factory.SubFactory(
        factory='test_utils.factories.tags.TagFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginTag


class PluginReleaseDownloadRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PluginReleaseDownloadRequirement objects."""

    plugin_release = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginReleaseFactory',
    )
    download_requirement = factory.SubFactory(
        factory='test_utils.factories.requirements.DownloadRequirement',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleaseDownloadRequirement


class PluginReleasePackageRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PluginReleasePackageRequirement objects."""

    plugin_release = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginReleaseFactory',
    )
    package_requirement = factory.SubFactory(
        factory='test_utils.factories.packages.PackageFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleasePackageRequirement


class PluginReleasePyPiRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PluginReleasePyPiRequirement objects."""

    plugin_release = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginReleaseFactory',
    )
    pypi_requirement = factory.SubFactory(
        factory='test_utils.factories.requirements.PyPiRequirement',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleasePyPiRequirement


class PluginReleaseVersionControlRequirementFactory(
    factory.django.DjangoModelFactory
):
    """Model factory to use when testing with PluginReleaseVersionControlRequirement objects."""

    plugin_release = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginReleaseFactory',
    )
    vcs_requirement = factory.SubFactory(
        factory='test_utils.factories.requirements.VersionControlRequirementFactory',
    )

    class Meta:
        """Define the metaclass attributes."""

        model = PluginReleaseVersionControlRequirement


class SubPluginPathFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with SubPluginPath objects."""

    plugin = factory.SubFactory(
        factory='test_utils.factories.plugins.PluginFactory',
    )
    path = factory.Sequence(function=lambda n: f'some/path/{n}')

    class Meta:
        """Define the metaclass attributes."""

        model = SubPluginPath
