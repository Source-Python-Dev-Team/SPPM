# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.plugins.models import (
    Plugin,
    PluginTag,
)
from tags.models import Tag
from test_utils.factories.plugins import PluginTagFactory
from test_utils.helpers import get_new_fields_for_model


# =============================================================================
# TEST CASES
# =============================================================================
class PluginTagTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTupleEqual(
            tuple1=PluginTag.__bases__,
            tuple2=(AbstractUUIDPrimaryKeyModel,),
        )

    def test_field_names(self):
        self.assertSetEqual(
            set1=get_new_fields_for_model(PluginTag),
            set2={
                "plugin",
                "tag",
            },
        )

    def test_plugin_field(self):
        field = PluginTag._meta.get_field("plugin")
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Plugin,
        )
        self.assertEqual(
            first=getattr(field.remote_field, "on_delete"),
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_tag_field(self):
        field = PluginTag._meta.get_field("tag")
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Tag,
        )
        self.assertEqual(
            first=getattr(field.remote_field, "on_delete"),
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PluginTagFactory()
        self.assertEqual(
            first=str(obj),
            second=f"{obj.plugin} Tag: {obj.tag}",
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=getattr(PluginTag._meta, "unique_together"),
            tuple2=(("plugin", "tag"),),
        )
        self.assertEqual(
            first=PluginTag._meta.verbose_name,
            second="Plugin Tag",
        )
        self.assertEqual(
            first=PluginTag._meta.verbose_name_plural,
            second="Plugin Tags",
        )
