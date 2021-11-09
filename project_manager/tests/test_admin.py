# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.test import TestCase

# Third Party Django
from precise_bbcode.models import BBCodeTag, SmileyTag

# App
from project_manager.packages.models import Package
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# TEST CASES
# =============================================================================
class AdminTestCase(TestCase):
    def test_project_admins_are_registered(self):
        self.assertIn(
            member=Package,
            container=admin.site._registry,
        )
        self.assertIn(
            member=Plugin,
            container=admin.site._registry,
        )
        self.assertIn(
            member=SubPlugin,
            container=admin.site._registry,
        )

    def test_third_party_models_not_registered(self):
        self.assertNotIn(
            member=Group,
            container=admin.site._registry,
        )
        self.assertNotIn(
            member=BBCodeTag,
            container=admin.site._registry,
        )
        self.assertNotIn(
            member=SmileyTag,
            container=admin.site._registry,
        )
