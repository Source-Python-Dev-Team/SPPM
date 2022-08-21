# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.packages.models import (
    Package,
    PackageContributor,
)
from test_utils.factories.packages import (
    PackageContributorFactory,
    PackageFactory,
)
from test_utils.factories.users import ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class PackageContributorTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageContributor, AbstractUUIDPrimaryKeyModel)
        )

    def test_package_field(self):
        field = PackageContributor._meta.get_field('package')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Package,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_user_field(self):
        field = PackageContributor._meta.get_field('user')
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
        obj = PackageContributorFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.package} Contributor: {obj.user}',
        )

    def test_clean(self):
        owner = ForumUserFactory()
        contributor = ForumUserFactory()
        package = PackageFactory(owner=owner)
        PackageContributor(
            user=contributor,
            package=package,
        ).clean()

        with self.assertRaises(ValidationError) as context:
            PackageContributor(
                user=owner,
                package=package,
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
            tuple1=PackageContributor._meta.unique_together,
            tuple2=(('package', 'user'),),
        )
        self.assertEqual(
            first=PackageContributor._meta.verbose_name,
            second='Package Contributor',
        )
        self.assertEqual(
            first=PackageContributor._meta.verbose_name_plural,
            second='Package Contributors',
        )
