# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.plugins.constants import PATH_MAX_LENGTH
from project_manager.plugins.models import (
    Plugin,
    SubPluginPath,
)
from project_manager.plugins.validators import sub_plugin_path_validator
from test_utils.factories.plugins import (
    PluginFactory,
    SubPluginPathFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginPathTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginPath, AbstractUUIDPrimaryKeyModel))

    def test_plugin_field(self):
        field = SubPluginPath._meta.get_field('plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Plugin,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='paths',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )

    def test_path_field(self):
        field = SubPluginPath._meta.get_field('path')
        self.assertIsInstance(obj=field, cls=models.CharField)
        self.assertEqual(
            first=field.max_length,
            second=PATH_MAX_LENGTH,
        )
        self.assertIn(
            member=sub_plugin_path_validator,
            container=field.validators,
        )

    def test_allow_module_field(self):
        field = SubPluginPath._meta.get_field('allow_module')
        self.assertIsInstance(obj=field, cls=models.BooleanField)
        self.assertFalse(expr=field.default)

    def test_allow_package_using_basename_field(self):
        field = SubPluginPath._meta.get_field('allow_package_using_basename')
        self.assertIsInstance(obj=field, cls=models.BooleanField)
        self.assertFalse(expr=field.default)

    def test_allow_package_using_init_field(self):
        field = SubPluginPath._meta.get_field('allow_package_using_init')
        self.assertIsInstance(obj=field, cls=models.BooleanField)
        self.assertFalse(expr=field.default)

    def test__str__(self):
        path = SubPluginPathFactory()
        self.assertEqual(
            first=str(path),
            second=path.path,
        )

    def test_clean(self):
        SubPluginPath(
            allow_module=True,
            allow_package_using_basename=False,
            allow_package_using_init=False,
        ).clean()
        SubPluginPath(
            allow_module=False,
            allow_package_using_basename=True,
            allow_package_using_init=False,
        ).clean()
        SubPluginPath(
            allow_module=False,
            allow_package_using_basename=False,
            allow_package_using_init=True,
        ).clean()
        with self.assertRaises(ValidationError) as context:
            SubPluginPath(
                allow_module=False,
                allow_package_using_basename=False,
                allow_package_using_init=False,
            ).clean()

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=3,
        )
        for attribute in (
            'allow_module',
            'allow_package_using_basename',
            'allow_package_using_init',
        ):
            self.assertIn(
                member=attribute,
                container=context.exception.message_dict,
            )
            self.assertEqual(
                first=len(context.exception.message_dict[attribute]),
                second=1,
            )
            self.assertEqual(
                first=context.exception.message_dict[attribute][0],
                second='At least one of the "Allow" fields must be True.',
            )

        plugin = PluginFactory()
        path_1 = SubPluginPathFactory(
            path='path_1',
            plugin=plugin,
            allow_module=True,
        )
        SubPluginPathFactory(
            path='path_2',
            plugin=plugin,
        )

        path_1.path = 'path_3'
        path_1.clean()

        path_1.path = 'path_2'
        with self.assertRaises(ValidationError) as context:
            path_1.clean()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={'path': ['Path already exists for plugin.']}
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginPath._meta.unique_together,
            tuple2=(('path', 'plugin'),),
        )
        self.assertEqual(
            first=SubPluginPath._meta.verbose_name,
            second='SubPlugin Path',
        )
        self.assertEqual(
            first=SubPluginPath._meta.verbose_name_plural,
            second='SubPlugin Paths',
        )
