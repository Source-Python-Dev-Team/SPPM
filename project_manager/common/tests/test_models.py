# =============================================================================
# IMPORTS
# =============================================================================
# Python
from uuid import uuid4

# Django
from django.db import models
from django.test import TestCase

# Third Party Django
from embed_video.fields import EmbedVideoField
from model_utils.fields import AutoCreatedField
from precise_bbcode.fields import BBCodeTextField

# App
from project_manager.common.constants import (
    PROJECT_CONFIGURATION_MAX_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_SYNOPSIS_MAX_LENGTH,
    RELEASE_NOTES_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from project_manager.common.helpers import (
    handle_project_logo_upload,
    handle_release_zip_file_upload,
)
from project_manager.common.models import (
    AbstractUUIDPrimaryKeyModel,
    Project,
    ProjectRelease,
)
from project_manager.common.validators import version_validator


# =============================================================================
# TEST CASES
# =============================================================================
class AbstractUUIDPrimaryKeyModelTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(AbstractUUIDPrimaryKeyModel, models.Model)
        )

    def test_id_field(self):
        field = AbstractUUIDPrimaryKeyModel._meta.get_field('id')
        self.assertIsInstance(
            obj=field,
            cls=models.UUIDField,
        )
        self.assertTrue(expr=field.primary_key)
        self.assertFalse(expr=field.editable)
        self.assertEqual(
            first=field.verbose_name,
            second='ID',
        )
        self.assertEqual(
            first=field.default,
            second=uuid4,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=AbstractUUIDPrimaryKeyModel._meta.abstract
        )


class ProjectTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(expr=issubclass(Project, models.Model))

    def test_name_field(self):
        field = Project._meta.get_field('name')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=PROJECT_NAME_MAX_LENGTH,
        )
        self.assertEqual(
            first=field.help_text,
            second=(
                "The name of the project. Do not include the version, as that "
                "is added dynamically to the project's page."
            ),
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_configuration_field(self):
        field = Project._meta.get_field('configuration')
        self.assertIsInstance(
            obj=field,
            cls=BBCodeTextField,
        )
        self.assertEqual(
            first=field.max_length,
            second=PROJECT_CONFIGURATION_MAX_LENGTH,
        )
        self.assertEqual(
            first=field.help_text,
            second=(
                'The configuration of the project. If too long, post on the '
                'forum and provide the link here. BBCode is allowed. 1024 '
                'char limit.'
            ),
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_description_field(self):
        field = Project._meta.get_field('description')
        self.assertIsInstance(
            obj=field,
            cls=BBCodeTextField,
        )
        self.assertEqual(
            first=field.max_length,
            second=PROJECT_DESCRIPTION_MAX_LENGTH,
        )
        self.assertEqual(
            first=field.help_text,
            second=(
                'The full description of the project. BBCode is allowed. '
                '1024 char limit.'
            ),
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_image_field(self):
        field = Project._meta.get_field('logo')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_project_logo_upload,
        )
        self.assertEqual(
            first=field.help_text,
            second="The project's logo image.",
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_video_field(self):
        field = Project._meta.get_field('video')
        self.assertIsInstance(
            obj=field,
            cls=EmbedVideoField,
        )
        self.assertEqual(
            first=field.help_text,
            second="The project's video.",
        )
        self.assertFalse(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_synopsis_field(self):
        field = Project._meta.get_field('synopsis')
        self.assertIsInstance(
            obj=field,
            cls=BBCodeTextField,
        )
        self.assertEqual(
            first=field.max_length,
            second=PROJECT_SYNOPSIS_MAX_LENGTH,
        )
        self.assertEqual(
            first=field.help_text,
            second=(
                'A brief description of the project. BBCode is allowed. '
                '128 char limit.'
            ),
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_topic_field(self):
        field = Project._meta.get_field('topic')
        self.assertIsInstance(
            obj=field,
            cls=models.IntegerField,
        )
        self.assertTrue(expr=field.unique)
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_created_field(self):
        field = Project._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=models.DateTimeField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_updated_field(self):
        field = Project._meta.get_field('updated')
        self.assertIsInstance(
            obj=field,
            cls=models.DateTimeField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='updated',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_handle_logo_upload_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            Project.handle_logo_upload.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"handle_logo_upload" attribute.'
            ),
        )

    def test_releases_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            Project.releases.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a "releases"'
                f' field via ForeignKey relationship.'
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=Project._meta.abstract
        )


class ProjectReleaseTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectRelease, AbstractUUIDPrimaryKeyModel),
        )

    def test_version_field(self):
        field = ProjectRelease._meta.get_field('version')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=RELEASE_VERSION_MAX_LENGTH,
        )
        self.assertIn(
            member=version_validator,
            container=field.validators,
        )
        self.assertEqual(
            first=field.help_text,
            second='The version for this release of the project.',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_notes_field(self):
        field = ProjectRelease._meta.get_field('notes')
        self.assertIsInstance(
            obj=field,
            cls=BBCodeTextField,
        )
        self.assertEqual(
            first=field.max_length,
            second=RELEASE_NOTES_MAX_LENGTH,
        )
        self.assertEqual(
            first=field.help_text,
            second='The notes for this particular release of the project.',
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_zip_file_field(self):
        field = ProjectRelease._meta.get_field('zip_file')
        self.assertIsInstance(
            obj=field,
            cls=models.FileField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_release_zip_file_upload,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_download_count_field(self):
        field = ProjectRelease._meta.get_field('download_count')
        self.assertIsInstance(
            obj=field,
            cls=models.PositiveIntegerField,
        )
        self.assertEqual(
            first=field.default,
            second=0,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_field(self):
        field = ProjectRelease._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=AutoCreatedField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )

    def test_project_class_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectRelease.project_class.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_class" attribute.'
            ),
        )

    def test_project_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectRelease.project.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a "project"'
                f' property.'
            ),
        )

    def test_handle_zip_file_upload_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectRelease.handle_zip_file_upload.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"handle_zip_file_upload" attribute.'
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectRelease._meta.abstract
        )
