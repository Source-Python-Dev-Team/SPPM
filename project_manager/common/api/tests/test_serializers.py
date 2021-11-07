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
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.serializers.mixins import (
    AddProjectToViewMixin,
    ProjectLocaleMixin,
    ProjectThroughMixin,
)
from test_utils.factories.users import ForumUserFactory


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


class AddProjectToViewMixinTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(AddProjectToViewMixin, ModelSerializer),
        )

    def test_validate(self):
        project_type = 'test-type'
        project = mock.Mock()
        obj = AddProjectToViewMixin(
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
