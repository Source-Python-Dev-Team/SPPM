# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from operator import attrgetter

# Django
from django import forms
from django.test import TestCase

# App
from ...models import ForumUser
from ..forms import (
    PackageCreateForm, PackageEditForm, PackageSelectGamesForm,
    PackageUpdateForm,
)
from ..models import Package, PackageRelease


# =============================================================================
# >> TESTS
# =============================================================================
class TestPackageCreateForm(TestCase):
    def test_name_is_required(self):
        form = PackageCreateForm(data={
            'name': None,
        })
        self.assertFalse(
            form.is_valid(),
            msg='Form should not be valid because name is required.',
        )
        self.assertIn(
            member='name',
            container=form.errors.as_data(),
        )
        self.assertIn(
            member='required',
            container=map(
                attrgetter('code'),
                form.errors.as_data()['name'],
            ),
            msg='name should be required.'
        )

    def test_version_is_required(self):
        form = PackageCreateForm(data={
            'version': None,
        })
        self.assertFalse(
            form.is_valid(),
            msg='Form should not be valid because version is required.',
        )
        self.assertIn(
            member='version',
            container=form.errors.as_data(),
        )
        self.assertIn(
            member='required',
            container=map(
                attrgetter('code'),
                form.errors.as_data()['version'],
            ),
            msg='version should be required.'
        )

    def test_zip_file_is_required(self):
        form = PackageCreateForm(data={
            'zip_file': None,
        })
        self.assertFalse(
            form.is_valid(),
            msg='Form should not be valid because zip_file is required.',
        )
        self.assertIn(
            member='zip_file',
            container=form.errors.as_data(),
        )
        self.assertIn(
            member='required',
            container=map(
                attrgetter('code'),
                form.errors.as_data()['zip_file'],
            ),
            msg='zip_file should be required.'
        )

    def test_slug_is_hidden(self):
        form = PackageCreateForm()
        self.assertTrue(
            isinstance(
                form.fields['slug'].widget,
                forms.HiddenInput,
            ),
            msg='slug should be hidden.'
        )


class TestPackageEditForm(TestCase):
    def test_nothing_is_required(self):
        form = PackageEditForm(data={})
        self.assertTrue(form.is_valid())


class TestPackageUpdateForm(TestCase):
    def test_version_is_required(self):
        form = PackageUpdateForm(data={
            'version': None,
        })
        self.assertFalse(
            form.is_valid(),
            msg='Form should not be valid because version is required.',
        )
        self.assertIn(
            member='version',
            container=form.errors.as_data(),
        )
        self.assertIn(
            member='required',
            container=map(
                attrgetter('code'),
                form.errors.as_data()['version'],
            ),
            msg='version should be required.'
        )

    def test_zip_file_is_required(self):
        form = PackageUpdateForm(data={
            'zip_file': None,
        })
        self.assertFalse(
            form.is_valid(),
            msg='Form should not be valid because zip_file is required.',
        )
        self.assertIn(
            member='zip_file',
            container=form.errors.as_data(),
        )
        self.assertIn(
            member='required',
            container=map(
                attrgetter('code'),
                form.errors.as_data()['zip_file'],
            ),
            msg='zip_file should be required.'
        )

    def test_version_must_be_unique_for_package(self):
        user = ForumUser.objects.create(
            username='test',
            id=1,
        )
        package = Package.objects.create(
            name='Test',
            basename='test',
            owner=user,
        )
        PackageRelease.objects.create(
            package=package,
            version='1.0',
            zip_file='{slug}/{slug}-v1.0.zip'.format(slug=package.slug)
        )
        form = PackageUpdateForm(data={
            'version': '1.0',
        })
        form.instance = package
        self.assertFalse(
            form.is_valid(),
            msg='Form should not be valid because version must be unique.',
        )
        self.assertIn(
            member='version',
            container=form.errors.as_data(),
        )
        self.assertIn(
            member='duplicate',
            container=map(
                attrgetter('code'),
                form.errors.as_data()['version'],
            ),
            msg='version should be unique for package.'
        )


class TestPackageSelectGamesForm(TestCase):
    pass
