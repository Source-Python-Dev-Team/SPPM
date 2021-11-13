# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from project_manager.common.api.views.mixins import (
    ProjectRelatedInfoMixin,
    ProjectThroughModelMixin,
)
from project_manager.common.constants import RELEASE_VERSION_REGEX


# =============================================================================
# TEST CASES
# =============================================================================
class ProjectRelatedInfoMixinTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(ProjectRelatedInfoMixin, ModelViewSet))

    def test_primary_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectRelatedInfoMixin.filter_backends,
            tuple2=(OrderingFilter, DjangoFilterBackend),
        )

    def test_project_type_required(self):
        obj = ProjectRelatedInfoMixin()
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.project_type

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_type" attribute.'
            ),
        )

    def test_project_model_required(self):
        obj = ProjectRelatedInfoMixin()
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.project_model

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_model" attribute.'
            ),
        )


class ProjectThroughModelMixinTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(ProjectThroughModelMixin, ModelViewSet))

    def test_primary_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectThroughModelMixin.authentication_classes,
            tuple2=(SessionAuthentication,),
        )
        self.assertTupleEqual(
            tuple1=ProjectThroughModelMixin.http_method_names,
            tuple2=('get', 'post', 'delete', 'options'),
        )
        self.assertTupleEqual(
            tuple1=ProjectThroughModelMixin.permission_classes,
            tuple2=(IsAuthenticatedOrReadOnly,),
        )


class ProjectAPIViewTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(ProjectAPIView, APIView))

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=ProjectAPIView.http_method_names,
            tuple2=('get', 'options'),
        )


class ProjectViewSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(ProjectViewSet, ModelViewSet))

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectViewSet.authentication_classes,
            tuple2=(SessionAuthentication,),
        )
        self.assertTupleEqual(
            tuple1=ProjectViewSet.filter_backends,
            tuple2=(OrderingFilter, DjangoFilterBackend),
        )
        self.assertTupleEqual(
            tuple1=ProjectViewSet.http_method_names,
            tuple2=('get', 'post', 'patch', 'options'),
        )
        self.assertTupleEqual(
            tuple1=ProjectViewSet.ordering,
            tuple2=('-releases__created',),
        )
        self.assertTupleEqual(
            tuple1=ProjectViewSet.ordering_fields,
            tuple2=('name', 'basename', 'updated', 'created'),
        )
        self.assertTupleEqual(
            tuple1=ProjectViewSet.permission_classes,
            tuple2=(IsAuthenticatedOrReadOnly,),
        )

    def test_creation_serializer_class_required(self):
        obj = ProjectViewSet()
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.creation_serializer_class

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"creation_serializer_class" attribute.'
            ),
        )


class ProjectImageViewSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectImageViewSet, ProjectThroughModelMixin),
        )

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectImageViewSet.ordering,
            tuple2=('-created',),
        )
        self.assertTupleEqual(
            tuple1=ProjectImageViewSet.ordering_fields,
            tuple2=('created',),
        )
        self.assertEqual(
            first=ProjectImageViewSet.related_model_type,
            second='Image',
        )


class ProjectReleaseViewSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectReleaseViewSet, ProjectRelatedInfoMixin),
        )

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectReleaseViewSet.http_method_names,
            tuple2=('get', 'post', 'options'),
        )
        self.assertTupleEqual(
            tuple1=ProjectReleaseViewSet.ordering,
            tuple2=('-created',),
        )
        self.assertTupleEqual(
            tuple1=ProjectReleaseViewSet.ordering_fields,
            tuple2=('created',),
        )
        self.assertEqual(
            first=ProjectReleaseViewSet.lookup_value_regex,
            second=RELEASE_VERSION_REGEX,
        )
        self.assertEqual(
            first=ProjectReleaseViewSet.lookup_field,
            second='version',
        )
        self.assertEqual(
            first=ProjectReleaseViewSet.related_model_type,
            second='Release',
        )


class ProjectGameViewSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectGameViewSet, ProjectThroughModelMixin),
        )

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectGameViewSet.ordering,
            tuple2=('-game',),
        )
        self.assertTupleEqual(
            tuple1=ProjectGameViewSet.ordering_fields,
            tuple2=('game',),
        )
        self.assertEqual(
            first=ProjectGameViewSet.related_model_type,
            second='Game',
        )


class ProjectTagViewSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectTagViewSet, ProjectThroughModelMixin),
        )

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectTagViewSet.ordering,
            tuple2=('-tag',),
        )
        self.assertTupleEqual(
            tuple1=ProjectTagViewSet.ordering_fields,
            tuple2=('tag',),
        )
        self.assertEqual(
            first=ProjectTagViewSet.related_model_type,
            second='Tag',
        )


class ProjectContributorViewSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                ProjectContributorViewSet,
                ProjectThroughModelMixin,
            ),
        )

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=ProjectContributorViewSet.ordering,
            tuple2=('-user',),
        )
        self.assertTupleEqual(
            tuple1=ProjectContributorViewSet.ordering_fields,
            tuple2=('user',),
        )
        self.assertEqual(
            first=ProjectContributorViewSet.related_model_type,
            second='Contributor',
        )
        self.assertTrue(expr=ProjectContributorViewSet.owner_only_id_access)
