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
from project_manager.plugins.helpers import handle_plugin_image_upload
from project_manager.plugins.models import (
    Plugin,
    PluginImage,
)
from test_utils.factories.plugins import PluginImageFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginImage, AbstractUUIDPrimaryKeyModel)
        )

    def test_plugin_field(self):
        field = PluginImage._meta.get_field('plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Plugin,
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
        field = PluginImage._meta.get_field('image')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_plugin_image_upload,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_field(self):
        field = PluginImage._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=AutoCreatedField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )

    def test__str__(self):
        obj = PluginImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.plugin} - {obj.image}',
        )

    def test_meta_class(self):
        self.assertEqual(
            first=PluginImage._meta.verbose_name,
            second='Plugin Image',
        )
        self.assertEqual(
            first=PluginImage._meta.verbose_name_plural,
            second='Plugin Images',
        )
