# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase
from django.utils import formats
from django.utils.timezone import now

# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.serializers.mixins import (
    AddProjectToViewMixin,
    ProjectLocaleMixin,
    ProjectThroughMixin,
)


# =============================================================================
# TEST CASES
# =============================================================================
class ProjectLocaleMixinTestCase(TestCase):
    def test_get_date_time_dict(self):
        self.assertDictEqual(
            d1=ProjectLocaleMixin().get_date_time_dict(timestamp=None),
            d2={
                'actual': None,
                'locale': None,
                'locale_short': None,
            },
        )
        timestamp = now()
        self.assertDictEqual(
            d1=ProjectLocaleMixin().get_date_time_dict(timestamp=timestamp),
            d2={
                'actual': timestamp,
                'locale': formats.date_format(
                    value=timestamp,
                    format='DATETIME_FORMAT',
                ),
                'locale_short': formats.date_format(
                    value=timestamp,
                    format='SHORT_DATETIME_FORMAT',
                ),
            },
        )


class ProjectThroughMixinTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectThroughMixin, ModelSerializer),
        )


class AddProjectToViewMixinTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(AddProjectToViewMixin, ModelSerializer),
        )
