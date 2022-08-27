# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.constants import PYPI_URL
from requirements.constants import (
    REQUIREMENT_NAME_MAX_LENGTH,
    REQUIREMENT_SLUG_MAX_LENGTH,
    REQUIREMENT_URL_MAX_LENGTH,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.requirements import (
    DownloadRequirementFactory,
    PyPiRequirementFactory,
    VersionControlRequirementFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class DownloadRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(DownloadRequirement, models.Model),
        )

    def test_url_field(self):
        field = DownloadRequirement._meta.get_field('url')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=REQUIREMENT_URL_MAX_LENGTH,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertEqual(
            first=DownloadRequirement._meta.verbose_name,
            second='Download Requirement',
        )
        self.assertEqual(
            first=DownloadRequirement._meta.verbose_name_plural,
            second='Download Requirements',
        )

    def test__str__(self):
        download_requirement = DownloadRequirementFactory()
        self.assertEqual(
            first=str(download_requirement),
            second=download_requirement.url,
        )


class PyPiRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PyPiRequirement, models.Model),
        )

    def test_name_field(self):
        field = PyPiRequirement._meta.get_field('name')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=REQUIREMENT_NAME_MAX_LENGTH,
        )
        self.assertTrue(expr=field.unique)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_slug_field(self):
        field = PyPiRequirement._meta.get_field('slug')
        self.assertIsInstance(
            obj=field,
            cls=models.SlugField,
        )
        self.assertEqual(
            first=field.max_length,
            second=REQUIREMENT_SLUG_MAX_LENGTH,
        )
        self.assertTrue(expr=field.unique)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertEqual(
            first=PyPiRequirement._meta.verbose_name,
            second='PyPi Requirement',
        )
        self.assertEqual(
            first=PyPiRequirement._meta.verbose_name_plural,
            second='PyPi Requirements',
        )

    def test__str__(self):
        pypi_requirement = PyPiRequirementFactory()
        self.assertEqual(
            first=str(pypi_requirement),
            second=pypi_requirement.name,
        )

    def test_get_pypi_url(self):
        pypi_requirement = PyPiRequirementFactory()
        self.assertEqual(
            first=pypi_requirement.get_pypi_url(),
            second=PYPI_URL + f'/{pypi_requirement.name}'
        )


class VersionControlRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(VersionControlRequirement, models.Model),
        )

    def test_url_field(self):
        field = VersionControlRequirement._meta.get_field('url')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=REQUIREMENT_URL_MAX_LENGTH,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertEqual(
            first=VersionControlRequirement._meta.verbose_name,
            second='Version Control Requirement',
        )
        self.assertEqual(
            first=VersionControlRequirement._meta.verbose_name_plural,
            second='Version Control Requirements',
        )

    def test__str__(self):
        vcs_requirement = VersionControlRequirementFactory()
        self.assertEqual(
            first=str(vcs_requirement),
            second=vcs_requirement.url,
        )
