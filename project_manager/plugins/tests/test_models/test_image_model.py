# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import ProjectImage
from project_manager.plugins.models import (
    Plugin,
    PluginImage,
)
from test_utils.factories.plugins import PluginImageFactory
from test_utils.helpers import get_new_fields_for_model


# =============================================================================
# TEST CASES
# =============================================================================
class PluginImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTupleEqual(
            tuple1=PluginImage.__bases__,
            tuple2=(ProjectImage,),
        )

    def test_field_names(self):
        self.assertSetEqual(
            set1=get_new_fields_for_model(PluginImage),
            set2={
                "plugin",
            },
        )

    def test_plugin_field(self):
        field = PluginImage._meta.get_field("plugin")
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
        self.assertEqual(
            first=getattr(field.remote_field, "related_name"),
            second="images",
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PluginImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f"{obj.plugin} - {obj.image}",
        )

    def test_meta_class(self):
        self.assertEqual(
            first=PluginImage._meta.verbose_name,
            second="Plugin Image",
        )
        self.assertEqual(
            first=PluginImage._meta.verbose_name_plural,
            second="Plugin Images",
        )
