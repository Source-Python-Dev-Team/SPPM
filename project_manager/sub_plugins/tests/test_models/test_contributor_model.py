# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
)
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
)
from test_utils.factories.users import ForumUserFactory
from test_utils.helpers import get_new_fields_for_model
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginContributorTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTupleEqual(
            tuple1=SubPluginContributor.__bases__,
            tuple2=(AbstractUUIDPrimaryKeyModel,),
        )

    def test_field_names(self):
        self.assertSetEqual(
            set1=get_new_fields_for_model(SubPluginContributor),
            set2={
                "sub_plugin",
                "user",
            },
        )

    def test_sub_plugin_field(self):
        field = SubPluginContributor._meta.get_field("sub_plugin")
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_user_field(self):
        field = SubPluginContributor._meta.get_field("user")
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=ForumUser,
        )
        self.assertEqual(
            first=getattr(field.remote_field, "on_delete"),
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = SubPluginContributorFactory()
        self.assertEqual(
            first=str(obj),
            second=f"{obj.sub_plugin} Contributor: {obj.user}",
        )

    def test_clean(self):
        owner = ForumUserFactory()
        contributor = ForumUserFactory()
        sub_plugin = SubPluginFactory(owner=owner)
        SubPluginContributor(
            user=contributor,
            sub_plugin=sub_plugin,
        ).clean()

        with self.assertRaises(ValidationError) as context:
            SubPluginContributor(
                user=owner,
                sub_plugin=sub_plugin,
            ).clean()

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=1,
        )
        self.assertIn(
            member="user",
            container=context.exception.message_dict,
        )
        self.assertEqual(
            first=len(context.exception.message_dict["user"]),
            second=1,
        )
        self.assertEqual(
            first=context.exception.message_dict["user"][0],
            second=(
                f"{owner} is the owner and cannot be added as a contributor."
            ),
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=getattr(SubPluginContributor._meta, "unique_together"),
            tuple2=(("sub_plugin", "user"),),
        )
        self.assertEqual(
            first=SubPluginContributor._meta.verbose_name,
            second="SubPlugin Contributor",
        )
        self.assertEqual(
            first=SubPluginContributor._meta.verbose_name_plural,
            second="SubPlugin Contributors",
        )
