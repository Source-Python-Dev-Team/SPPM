# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.db import models
from django.test import TestCase

# App
from tags.constants import TAG_NAME_MAX_LENGTH
from tags.models import Tag
from tags.validators import tag_name_validator
from test_utils.factories.tags import TagFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class GameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(Tag, models.Model),
        )

    def test_name_field(self):
        field = Tag._meta.get_field('name')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=TAG_NAME_MAX_LENGTH,
        )
        self.assertTrue(expr=field.primary_key)
        self.assertTrue(expr=field.unique)
        self.assertIn(
            member=tag_name_validator,
            container=field.validators,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_black_listed_field(self):
        field = Tag._meta.get_field('black_listed')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_creator_field(self):
        field = Tag._meta.get_field('creator')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=ForumUser,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='created_tags',
        )
        self.assertTrue(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertEqual(
            first=Tag._meta.verbose_name,
            second='Tag',
        )
        self.assertEqual(
            first=Tag._meta.verbose_name_plural,
            second='Tags',
        )

    def test__str__(self):
        tag = TagFactory()
        self.assertEqual(
            first=str(tag),
            second=tag.name,
        )

    @mock.patch.object(
        target=Tag,
        attribute='packagetag_set',
    )
    @mock.patch.object(
        target=Tag,
        attribute='plugintag_set',
    )
    @mock.patch.object(
        target=Tag,
        attribute='subplugintag_set',
    )
    def test_save_on_black_listed(
        self, sub_plugin_set, plugin_set, package_set
    ):
        tag = TagFactory()
        tag.black_listed = True
        tag.save()
        package_set.all.return_value.delete.assert_called_once_with()
        plugin_set.all.return_value.delete.assert_called_once_with()
        sub_plugin_set.all.return_value.delete.assert_called_once_with()
