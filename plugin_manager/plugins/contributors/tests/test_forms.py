# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from operator import attrgetter

# Django
from django import forms
from django.test import TestCase

# App
from plugin_manager.plugins.contributors.forms import (
    PluginAddContributorConfirmationForm
)


# =============================================================================
# >> TESTS
# =============================================================================
class TestPluginAddContributorConfirmationForm(TestCase):
    def test_id_is_required(self):
        form = PluginAddContributorConfirmationForm(data={
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
        form = PluginAddContributorConfirmationForm()
        self.assertTrue(
            isinstance(
                form.fields['id'].widget,
                forms.HiddenInput,
            ),
            msg='id should be hidden.'
        )
