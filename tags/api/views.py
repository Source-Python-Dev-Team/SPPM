"""Tag API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Count, F, Prefetch, QuerySet

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

# App
from project_manager.sub_plugins.models import SubPlugin
from tags.api.serializers import TagListSerializer, TagRetrieveSerializer
from tags.models import Tag

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "TagViewSet",
)


# =============================================================================
# VIEWS
# =============================================================================
class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet for listing Supported Games.

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)
    *  **project_count** (descending) or **-project_count** (ascending)

        ####Example:
        `?ordering=name`

        `?ordering=-project_count`
    """

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    queryset = Tag.objects.all()
    ordering = ("name",)
    ordering_fields = ("name", "project_count")
    http_method_names = ("get", "options")

    def retrieve(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict,
    ) -> Response:
        """Overwrite the ordering fields on retrieve to exclude project_count.

        This helps avoid a FieldError since project_count is an annotation
            that only occurs during the list view.
        """
        self.ordering_fields = ("name",)
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self) -> type[ModelSerializer]:
        """Return the correct serializer based on the action."""
        if self.action == "retrieve":
            return TagRetrieveSerializer

        return TagListSerializer

    def get_queryset(self) -> QuerySet:
        """Filter the queryset to not return black-listed tags."""
        queryset = super().get_queryset().filter(
            black_listed=False,
        )
        if self.action == "retrieve":
            return queryset.prefetch_related(
                Prefetch(
                    lookup="sub_plugins",
                    queryset=SubPlugin.objects.select_related(
                        "plugin",
                    ).order_by(
                        "name",
                    ),
                ),
            )

        return queryset.annotate(
            package_count=Count("packages", distinct=True),
            plugin_count=Count("plugins", distinct=True),
            sub_plugin_count=Count("sub_plugins", distinct=True),
            project_count=(
                F("package_count") + F("plugin_count") + F("sub_plugin_count")
            ),
        )
