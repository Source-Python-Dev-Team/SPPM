# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# App
from plugin_manager.plugins.views import (
    PluginCreateView, PluginEditView, PluginListView,
    PluginReleaseDownloadView, PluginReleaseListView, PluginSelectGamesView,
    PluginUpdateView, PluginView,
)
from plugin_manager.plugins.contributors.views import (
    PluginAddContributorConfirmationView, PluginAddContributorView,
)


# =============================================================================
# >> TESTS
# =============================================================================
class TestPluginAddContributorConfirmationView(TestCase):
    pass


class TestPluginAddContributorView(TestCase):
    pass


class TestPluginCreateView(TestCase):
    pass


class TestPluginEditView(TestCase):
    pass


class TestPluginListView(TestCase):
    pass


class TestPluginUpdateView(TestCase):
    pass


class TestPluginView(TestCase):
    pass


class TestPluginReleaseDownloadView(TestCase):
    pass


class TestPluginReleaseListView(TestCase):
    pass


class TestPluginSelectGamesView(TestCase):
    pass
