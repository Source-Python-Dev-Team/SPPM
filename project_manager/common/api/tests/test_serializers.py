# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.test import TestCase
from django.utils import formats
from django.utils.timezone import now

# Third Party Django
from rest_framework.fields import (
    CharField,
    FileField,
    IntegerField,
    SerializerMethodField,
)
from rest_framework.serializers import ModelSerializer

# App
from games.api.common.serializers import MinimalGameSerializer
from games.constants import GAME_SLUG_MAX_LENGTH
from project_manager.common.api.serializers import (
    ProjectContributorSerializer,
    ProjectCreateReleaseSerializer,
    ProjectGameSerializer,
    ProjectImageSerializer,
    ProjectReleaseSerializer,
    ProjectSerializer,
    ProjectTagSerializer,
)
from project_manager.common.api.serializers.mixins import (
    CreateRequirementsMixin,
    ProjectLocaleMixin,
    ProjectReleaseCreationMixin,
    ProjectThroughMixin,
)
from project_manager.common.constants import (
    RELEASE_NOTES_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from tags.constants import TAG_NAME_MAX_LENGTH
from test_utils.factories.users import ForumUserFactory
from users.api.common.serializers import ForumUserContributorSerializer
from users.constants import USER_USERNAME_MAX_LENGTH


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

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = ForumUserFactory()

    def setUp(self) -> None:
        super().setUp()
        self.field_names = (
            'name',
        )
        self.mock_get_field_names = mock.patch(
            target='rest_framework.serializers.ModelSerializer.get_field_names',
            return_value=self.field_names,
        ).start()

    def tearDown(self) -> None:
        super().tearDown()
        mock.patch.stopall()

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectThroughMixin, ModelSerializer),
        )

    def test_get_field_names_not_get(self):
        obj = ProjectThroughMixin(
            context={
                'request': mock.Mock(
                    method='POST',
                ),
            },
        )
        self.assertTupleEqual(
            tuple1=obj.get_field_names('', ''),
            tuple2=self.field_names,
        )

    def test_get_field_names_no_view(self):
        obj = ProjectThroughMixin(
            context={
                'request': mock.Mock(
                    method='GET',
                ),
            },
        )
        self.assertTupleEqual(
            tuple1=obj.get_field_names('', ''),
            tuple2=self.field_names,
        )

    def test_get_field_names_owner(self):
        obj = ProjectThroughMixin(
            context={
                'request': mock.Mock(
                    method='GET',
                    user=self.user.user,
                ),
                'view': mock.Mock(
                    owner=self.user.user.id,
                )
            },
        )
        self.assertTupleEqual(
            tuple1=obj.get_field_names('', ''),
            tuple2=self.field_names + ('id',),
        )

    def test_get_field_names_contributor(self):
        obj = ProjectThroughMixin(
            context={
                'request': mock.Mock(
                    method='GET',
                    user=self.user.user,
                ),
                'view': mock.Mock(
                    contributors=(self.user.user.id,),
                    owner_only_id_access=False,
                )
            },
        )
        self.assertTupleEqual(
            tuple1=obj.get_field_names('', ''),
            tuple2=self.field_names + ('id',),
        )

    def test_get_field_names_contributor_owner_only(self):
        obj = ProjectThroughMixin(
            context={
                'request': mock.Mock(
                    method='GET',
                    user=self.user.user,
                ),
                'view': mock.Mock(
                    contributors=(self.user.user.id,),
                    owner_only_id_access=True,
                ),
            },
        )
        self.assertTupleEqual(
            tuple1=obj.get_field_names('', ''),
            tuple2=self.field_names,
        )

    def test_validate(self):
        project_type = 'test-type'
        project = mock.Mock()
        obj = ProjectThroughMixin(
            context={
                'view': mock.Mock(
                    project_type=project_type,
                    project=project,
                ),
            },
        )
        original_attrs = {
            'field': 'value',
        }
        return_attrs = dict(original_attrs)
        return_attrs.update({
            project_type.replace('-', '_'): project,
        })
        self.assertDictEqual(
            d1=obj.validate(original_attrs),
            d2=return_attrs,
        )


class ProjectReleaseCreationMixinTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectReleaseCreationMixin, ModelSerializer),
        )
        self.assertTrue(
            expr=issubclass(ProjectReleaseCreationMixin, CreateRequirementsMixin),
        )

    def test_project_class_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectReleaseCreationMixin.project_class.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_class" attribute.'
            ),
        )

    def test_project_type_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectReleaseCreationMixin.project_type.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_type" attribute.'
            ),
        )

    def test_zip_parser_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectReleaseCreationMixin.zip_parser.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"zip_parser" attribute.'
            ),
        )

    def test_get_project_kwargs_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectReleaseCreationMixin.get_project_kwargs(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"get_project_kwargs" method.'
            ),
        )


class ProjectContributorSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectContributorSerializer, ProjectThroughMixin),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ProjectContributorSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=2,
        )

        self.assertIn(
            member='username',
            container=declared_fields,
        )
        field = declared_fields['username']
        self.assertIsInstance(
            obj=field,
            cls=CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=USER_USERNAME_MAX_LENGTH,
        )
        self.assertTrue(expr=field.write_only)

        self.assertIn(
            member='user',
            container=declared_fields,
        )
        field = declared_fields['user']
        self.assertIsInstance(
            obj=field,
            cls=ForumUserContributorSerializer,
        )
        self.assertTrue(expr=field.read_only)

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectContributorSerializer.Meta.fields,
            tuple2=('username', 'user'),
        )


class ProjectCreateReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectCreateReleaseSerializer, ProjectReleaseCreationMixin),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ProjectCreateReleaseSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=3,
        )

        self.assertIn(
            member='notes',
            container=declared_fields,
        )
        field = declared_fields['notes']
        self.assertIsInstance(
            obj=field,
            cls=CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=RELEASE_NOTES_MAX_LENGTH,
        )
        self.assertTrue(expr=field.allow_blank)

        self.assertIn(
            member='version',
            container=declared_fields,
        )
        field = declared_fields['version']
        self.assertIsInstance(
            obj=field,
            cls=CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=RELEASE_VERSION_MAX_LENGTH,
        )
        self.assertTrue(expr=field.allow_blank)

        self.assertIn(
            member='zip_file',
            container=declared_fields,
        )
        field = declared_fields['zip_file']
        self.assertIsInstance(
            obj=field,
            cls=FileField,
        )
        self.assertTrue(expr=field.allow_null)

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectCreateReleaseSerializer.Meta.fields,
            tuple2=('notes', 'zip_file', 'version'),
        )


class ProjectGameSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectGameSerializer, ProjectThroughMixin),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ProjectGameSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=2,
        )

        self.assertIn(
            member='game_slug',
            container=declared_fields,
        )
        field = declared_fields['game_slug']
        self.assertIsInstance(
            obj=field,
            cls=CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=GAME_SLUG_MAX_LENGTH,
        )
        self.assertTrue(expr=field.write_only)

        self.assertIn(
            member='game',
            container=declared_fields,
        )
        field = declared_fields['game']
        self.assertIsInstance(
            obj=field,
            cls=MinimalGameSerializer,
        )
        self.assertTrue(expr=field.read_only)

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectGameSerializer.Meta.fields,
            tuple2=('game_slug', 'game'),
        )


class ProjectImageSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectImageSerializer, ProjectThroughMixin),
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectImageSerializer.Meta.fields,
            tuple2=('image',),
        )


class ProjectReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectReleaseSerializer, ProjectReleaseCreationMixin),
        )
        self.assertTrue(
            expr=issubclass(ProjectReleaseSerializer, ProjectLocaleMixin),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ProjectReleaseSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=3,
        )

        self.assertIn(
            member='created',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['created'],
            cls=SerializerMethodField,
        )

        self.assertIn(
            member='created_by',
            container=declared_fields,
        )
        field = declared_fields['created_by']
        self.assertIsInstance(
            obj=field,
            cls=ForumUserContributorSerializer,
        )
        self.assertTrue(expr=field.read_only)

        self.assertIn(
            member='download_count',
            container=declared_fields,
        )
        field = declared_fields['download_count']
        self.assertIsInstance(
            obj=field,
            cls=IntegerField,
        )
        self.assertTrue(expr=field.read_only)

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectReleaseSerializer.Meta.fields,
            tuple2=(
                'notes',
                'zip_file',
                'version',
                'created',
                'created_by',
                'download_count',
                'download_requirements',
                'package_requirements',
                'pypi_requirements',
                'vcs_requirements',
                'id',
            ),
        )


class ProjectSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectSerializer, ModelSerializer),
        )
        self.assertTrue(
            expr=issubclass(ProjectSerializer, ProjectLocaleMixin),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ProjectSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=4,
        )

        self.assertIn(
            member='current_release',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['current_release'],
            cls=SerializerMethodField,
        )

        self.assertIn(
            member='owner',
            container=declared_fields,
        )
        field = declared_fields['owner']
        self.assertIsInstance(
            obj=field,
            cls=ForumUserContributorSerializer,
        )
        self.assertTrue(expr=field.read_only)

        self.assertIn(
            member='created',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['created'],
            cls=SerializerMethodField,
        )

        self.assertIn(
            member='updated',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['updated'],
            cls=SerializerMethodField,
        )

    def test_project_type_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectSerializer.project_type.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_type" attribute.'
            ),
        )

    def test_release_model_required(self):
        obj = ''
        with self.assertRaises(NotImplementedError) as context:
            ProjectSerializer.release_model.fget(obj)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"release_model" attribute.'
            ),
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'total_downloads',
                'current_release',
                'created',
                'updated',
                'synopsis',
                'description',
                'configuration',
                'logo',
                'video',
                'owner',
            ),
        )
        self.assertTupleEqual(
            tuple1=ProjectSerializer.Meta.read_only_fields,
            tuple2=('slug',),
        )


class ProjectTagSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectTagSerializer, ProjectThroughMixin),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ProjectTagSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=1,
        )

        self.assertIn(
            member='tag',
            container=declared_fields,
        )
        field = declared_fields['tag']
        self.assertIsInstance(
            obj=field,
            cls=CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=TAG_NAME_MAX_LENGTH,
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectTagSerializer.Meta.fields,
            tuple2=('tag',),
        )
