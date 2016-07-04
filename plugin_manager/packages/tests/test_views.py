# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# App
from plugin_manager.packages.views import (
    PackageCreateView, PackageEditView, PackageListView,
    PackageReleaseDownloadView, PackageReleaseListView, PackageSelectGamesView,
    PackageUpdateView, PackageView,
)
from plugin_manager.packages.contributors.views import (
    PackageAddContributorConfirmationView, PackageAddContributorView,
)


# =============================================================================
# >> TESTS
# =============================================================================
class TestPackageAddContributorConfirmationView(TestCase):
    pass


class TestPackageAddContributorView(TestCase):
    pass


class TestPackageCreateView(TestCase):
    pass


class TestPackageEditView(TestCase):
    pass


class TestPackageListView(TestCase):
    pass


class TestPackageUpdateView(TestCase):
    pass


class TestPackageView(TestCase):
    pass


class TestPackageReleaseDownloadView(TestCase):
    pass


class TestPackageReleaseListView(TestCase):
    pass


class TestPackageSelectGamesView(TestCase):
    pass
