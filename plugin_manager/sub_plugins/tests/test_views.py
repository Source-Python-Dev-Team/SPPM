# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# App
from plugin_manager.sub_plugins.views import (
    SubPluginCreateView, SubPluginListView, SubPluginEditView,
    SubPluginReleaseDownloadView, SubPluginReleaseListView,
    SubPluginSelectGamesView, SubPluginUpdateView, SubPluginView,
)
from plugin_manager.sub_plugins.contributors.views import (
    SubPluginAddContributorConfirmationView, SubPluginAddContributorView,
)


# =============================================================================
# >> TESTS
# =============================================================================
class TestSubPluginAddContributorConfirmationView(TestCase):
    pass


class TestSubPluginAddContributorView(TestCase):
    pass


class TestSubPluginCreateView(TestCase):
    pass


class TestSubPluginListView(TestCase):
    pass


class TestSubPluginEditView(TestCase):
    pass


class TestSubPluginUpdateView(TestCase):
    pass


class TestSubPluginView(TestCase):
    pass


class TestSubPluginReleaseDownloadView(TestCase):
    pass


class TestSubPluginReleaseListView(TestCase):
    pass


class TestSubPluginSelectGamesView(TestCase):
    pass
