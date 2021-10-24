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
    handle_project_image_upload,
    handle_project_logo_upload,
    handle_release_zip_file_upload,
)
from project_manager.common.models import (
    AbstractUUIDPrimaryKeyModel,
    Project,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectReleaseDownloadRequirement,
    ProjectReleasePackageRequirement,
    ProjectReleasePyPiRequirement,
    ProjectReleaseVersionControlRequirement,
    ProjectTag,
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

    def test_owner_field(self):
        field = Project._meta.get_field('owner')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='users.ForumUser',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='%(class)ss',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

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

    def test_meta_class(self):
        self.assertTrue(
            expr=Project._meta.abstract
        )


class ProjectContributorTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectContributor, AbstractUUIDPrimaryKeyModel),
        )

    def test_user_field(self):
        field = ProjectContributor._meta.get_field('user')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='users.ForumUser',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectContributor._meta.abstract
        )


class ProjectGameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectGame, AbstractUUIDPrimaryKeyModel),
        )

    def test_game_field(self):
        field = ProjectGame._meta.get_field('game')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='games.Game',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectGame._meta.abstract
        )


class ProjectImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectImage, AbstractUUIDPrimaryKeyModel),
        )

    def test_image_field(self):
        field = ProjectImage._meta.get_field('image')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_project_image_upload,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_field(self):
        field = ProjectImage._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=AutoCreatedField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectImage._meta.abstract
        )
        self.assertEqual(
            first=ProjectImage._meta.verbose_name,
            second='Image',
        )
        self.assertEqual(
            first=ProjectImage._meta.verbose_name_plural,
            second='Images',
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

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectRelease._meta.abstract
        )
        self.assertEqual(
            first=ProjectRelease._meta.verbose_name,
            second='Release',
        )
        self.assertEqual(
            first=ProjectRelease._meta.verbose_name_plural,
            second='Releases',
        )


class ProjectReleaseDownloadRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                ProjectReleaseDownloadRequirement,
                AbstractUUIDPrimaryKeyModel,
            ),
        )

    def test_download_requirement_field(self):
        field = ProjectReleaseDownloadRequirement._meta.get_field(
            'download_requirement',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='requirements.DownloadRequirement',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_optional_field(self):
        field = ProjectReleaseDownloadRequirement._meta.get_field('optional')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectReleaseDownloadRequirement._meta.abstract
        )


class ProjectReleasePackageRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                ProjectReleasePackageRequirement,
                AbstractUUIDPrimaryKeyModel,
            ),
        )

    def test_package_requirement_field(self):
        field = ProjectReleasePackageRequirement._meta.get_field(
            'package_requirement',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='project_manager.Package',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_version_field(self):
        field = ProjectReleasePackageRequirement._meta.get_field('version')
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
            second=(
                'The version of the custom package for this release of the '
                'project.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = ProjectReleasePackageRequirement._meta.get_field('optional')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectReleasePackageRequirement._meta.abstract
        )


class ProjectReleasePyPiRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                ProjectReleasePyPiRequirement,
                AbstractUUIDPrimaryKeyModel,
            ),
        )

    def test_pypi_requirement_field(self):
        field = ProjectReleasePyPiRequirement._meta.get_field(
            'pypi_requirement',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='requirements.PyPiRequirement',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_version_field(self):
        field = ProjectReleasePyPiRequirement._meta.get_field('version')
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
            second=(
                'The version of the PyPi package for this release of the '
                'project.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = ProjectReleasePyPiRequirement._meta.get_field('optional')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectReleasePyPiRequirement._meta.abstract
        )


class ProjectReleaseVersionControlRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                ProjectReleaseVersionControlRequirement,
                AbstractUUIDPrimaryKeyModel,
            ),
        )

    def test_vcs_requirement_field(self):
        field = ProjectReleaseVersionControlRequirement._meta.get_field(
            'vcs_requirement',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='requirements.VersionControlRequirement',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_version_field(self):
        field = ProjectReleaseVersionControlRequirement._meta.get_field(
            'version',
        )
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
            second=(
                'The version of the VCS package for this release of the '
                'project.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = ProjectReleaseVersionControlRequirement._meta.get_field(
            'optional',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=ProjectReleaseVersionControlRequirement._meta.abstract
        )


class ProjectTagTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectTag, AbstractUUIDPrimaryKeyModel),
        )

    def test_tag_field(self):
        field = ProjectTag._meta.get_field('tag')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='tags.Tag',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(expr=ProjectTag._meta.abstract)
