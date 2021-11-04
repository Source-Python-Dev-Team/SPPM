# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase
from django.views.generic import View

# App
from project_manager.common.mixins import DownloadMixin


# =============================================================================
# TEST CASES
# =============================================================================
class DownloadMixinTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(DownloadMixin, View),
        )

    def test_model_required(self):
        obj = DownloadMixin()
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.model

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"model" attribute.'
            ),
        )

    def test_base_url_required(self):
        obj = DownloadMixin()
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.base_url

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"base_url" attribute.'
            ),
        )

    def test_project_model_required(self):
        obj = DownloadMixin()
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.project_model

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_model" attribute.'
            ),
        )

    def test_model_kwarg_required(self):
        obj = DownloadMixin()
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.model_kwarg

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"model_kwarg" attribute.'
            ),
        )
