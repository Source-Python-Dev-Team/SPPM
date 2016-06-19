# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from ...users.models import ForumUser
from ..models import (
    OldPackageRelease,
    Package,
    PackageImage,
)


# =============================================================================
# >> TEST CLASSES
# =============================================================================
class TestOldPackageRelease(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_oldpackagerelease.package_id'
            ),
            OldPackageRelease.objects.create,
        )


class TestPackage(TestCase):
    def setUp(self):
        ForumUser.objects.create(username='test_user', id=1)
        Package.objects.create(name='Test', basename='test')

    def test_name_must_be_unique(self):
        self.assertRaises(
            IntegrityError,
            Package.objects.create,
            name='Test',
            basename='test2',
        )

    def test_basename_must_be_unique(self):
        self.assertRaises(
            IntegrityError,
            Package.objects.create,
            name='Test2',
            basename='test',
        )


class TestPackageImage(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_packageimage.package_id'
            ),
            PackageImage.objects.create,
        )
