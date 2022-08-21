# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
)
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
)
from test_utils.factories.users import ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class PluginContributorTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginContributor, AbstractUUIDPrimaryKeyModel)
        )

    def test_plugin_field(self):
        field = PluginContributor._meta.get_field('plugin')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_user_field(self):
        field = PluginContributor._meta.get_field('user')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PluginContributorFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.plugin} Contributor: {obj.user}',
        )

    def test_clean(self):
        owner = ForumUserFactory()
        contributor = ForumUserFactory()
        plugin = PluginFactory(owner=owner)
        PluginContributor(
            user=contributor,
            plugin=plugin,
        ).clean()

        with self.assertRaises(ValidationError) as context:
            PluginContributor(
                user=owner,
                plugin=plugin,
            ).clean()

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=1,
        )
        self.assertIn(
            member='user',
            container=context.exception.message_dict,
        )
        self.assertEqual(
            first=len(context.exception.message_dict['user']),
            second=1,
        )
        self.assertEqual(
            first=context.exception.message_dict['user'][0],
            second=(
                f'{owner} is the owner and cannot be added as a contributor.'
            ),
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginContributor._meta.unique_together,
            tuple2=(('plugin', 'user'),),
        )
        self.assertEqual(
            first=PluginContributor._meta.verbose_name,
            second='Plugin Contributor',
        )
        self.assertEqual(
            first=PluginContributor._meta.verbose_name_plural,
            second='Plugin Contributors',
        )
