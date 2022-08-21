# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginTag,
)
from tags.models import Tag
from test_utils.factories.sub_plugins import SubPluginTagFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginTagTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginTag, AbstractUUIDPrimaryKeyModel)
        )

    def test_sub_plugin_field(self):
        field = SubPluginTag._meta.get_field('sub_plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=SubPlugin,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_tag_field(self):
        field = SubPluginTag._meta.get_field('tag')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Tag,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = SubPluginTagFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.sub_plugin} Tag: {obj.tag}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginTag._meta.unique_together,
            tuple2=(('sub_plugin', 'tag'),),
        )
        self.assertEqual(
            first=SubPluginTag._meta.verbose_name,
            second='SubPlugin Tag',
        )
        self.assertEqual(
            first=SubPluginTag._meta.verbose_name_plural,
            second='SubPlugin Tags',
        )
