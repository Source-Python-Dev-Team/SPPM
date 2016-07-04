# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from operator import attrgetter

# Django
from django import forms
from django.test import TestCase

# App
from ..forms import (
    PackageAddContributorConfirmationForm, PackageCreateForm, PackageEditForm,
    PackageSelectGamesForm, PackageUpdateForm,
)


# =============================================================================
# >> TEST CLASSES
# =============================================================================
class TestPackageAddContributorConfirmationForm(TestCase):
    def test_id_is_required(self):
        form = PackageAddContributorConfirmationForm(data={
            'id': None,
        })
        self.assertFalse(
            form.is_valid(),
            msg='Form should not be valid because id is required.',
        )
        self.assertIn(
            member='id',
            container=form.errors.as_data(),
        )
        self.assertIn(
            member='required',
            container=map(
                attrgetter('code'),
                form.errors.as_data()['id'],
            ),
            msg='id should be required.'
        )

    def test_id_is_hidden(self):
        form = PackageAddContributorConfirmationForm()
        self.assertTrue(
            isinstance(
                form.fields['id'].widget,
                forms.HiddenInput,
            ),
            msg='id should be hidden.'
        )


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
    pass


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


class TestPackageSelectGamesForm(TestCase):
    pass
