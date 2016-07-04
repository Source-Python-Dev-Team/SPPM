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
    SubPluginAddContributorConfirmationForm, SubPluginCreateForm,
    SubPluginEditForm, SubPluginSelectGamesForm, SubPluginUpdateForm,
)


# =============================================================================
# >> TEST CLASSES
# =============================================================================
class TestSubPluginAddContributorConfirmationForm(TestCase):
    def test_id_is_required(self):
        form = SubPluginAddContributorConfirmationForm(data={
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
        form = SubPluginAddContributorConfirmationForm()
        self.assertTrue(
            isinstance(
                form.fields['id'].widget,
                forms.HiddenInput,
            ),
            msg='id should be hidden.'
        )


class TestSubPluginCreateForm(TestCase):
    def test_name_is_required(self):
        form = SubPluginCreateForm(data={
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
        form = SubPluginCreateForm(data={
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
        form = SubPluginCreateForm(data={
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
        form = SubPluginCreateForm()
        self.assertTrue(
            isinstance(
                form.fields['slug'].widget,
                forms.HiddenInput,
            ),
            msg='slug should be hidden.'
        )


class TestSubPluginEditForm(TestCase):
    pass


class TestSubPluginUpdateForm(TestCase):
    def test_version_is_required(self):
        form = SubPluginUpdateForm(data={
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
        form = SubPluginUpdateForm(data={
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


class TestSubPluginSelectGamesForm(TestCase):
    pass
