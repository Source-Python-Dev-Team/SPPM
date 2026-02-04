# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import ProjectImage
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginImage,
)
from test_utils.factories.sub_plugins import SubPluginImageFactory
from test_utils.helpers import get_new_fields_for_model


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTupleEqual(
            tuple1=SubPluginImage.__bases__,
            tuple2=(ProjectImage,),
        )

    def test_field_names(self):
        self.assertSetEqual(
            set1=get_new_fields_for_model(SubPluginImage),
            set2={
                "sub_plugin",
            },
        )

    def test_sub_plugin_field(self):
        field = SubPluginImage._meta.get_field("sub_plugin")
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=SubPlugin,
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
        obj = SubPluginImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f"{obj.sub_plugin} - {obj.image}",
        )

    def test_meta_class(self):
        self.assertEqual(
            first=SubPluginImage._meta.verbose_name,
            second="SubPlugin Image",
        )
        self.assertEqual(
            first=SubPluginImage._meta.verbose_name_plural,
            second="SubPlugin Images",
        )
