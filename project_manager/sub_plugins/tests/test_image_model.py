# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# Third Party Django
from model_utils.fields import AutoCreatedField

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.sub_plugins.helpers import handle_sub_plugin_image_upload
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginImage,
)
from test_utils.factories.sub_plugins import SubPluginImageFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginImage, AbstractUUIDPrimaryKeyModel)
        )

    def test_sub_plugin_field(self):
        field = SubPluginImage._meta.get_field('sub_plugin')
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
        self.assertEqual(
            first=field.remote_field.related_name,
            second='images',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_image_field(self):
        field = SubPluginImage._meta.get_field('image')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_sub_plugin_image_upload,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_field(self):
        field = SubPluginImage._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=AutoCreatedField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )

    def test__str__(self):
        obj = SubPluginImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.sub_plugin} - {obj.image}',
        )

    def test_meta_class(self):
        self.assertEqual(
            first=SubPluginImage._meta.verbose_name,
            second='SubPlugin Image',
        )
        self.assertEqual(
            first=SubPluginImage._meta.verbose_name_plural,
            second='SubPlugin Images',
        )
