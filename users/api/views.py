"""User API views."""

# =============================================================================
# IMPORTS
# =============================================================================
#  Django
from django.db.models import Prefetch

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

# App
from project_manager.packages.models import Package
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import SubPlugin
from users.api.filtersets import ForumUserFilterSet
from users.api.serializers import ForumUserSerializer
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserViewSet',
)


# =============================================================================
# VIEWS
# =============================================================================
class ForumUserViewSet(ModelViewSet):
    """ForumUser API view.

    ###Available Ordering:

    *  **forum_id** (descending) or **-forum_id** (ascending)
    *  **user__username** (descending) or **-user__username** (ascending)

        ####Example:
        `?ordering=forum_id`

        `?ordering=-user__username`
    """

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filterset_class = ForumUserFilterSet
    http_method_names = ('get', 'options')
    ordering = ('user__username',)
    ordering_fields = ('forum_id', 'user__username')
    queryset = ForumUser.objects.prefetch_related(
        Prefetch(
            lookup='packages',
            queryset=Package.objects.order_by(
                'name',
            )
        ),
        Prefetch(
            lookup='plugins',
            queryset=Plugin.objects.order_by(
                'name',
            )
        ),
        Prefetch(
            lookup='subplugins',
            queryset=SubPlugin.objects.order_by(
                'name',
            ).select_related(
                'plugin',
            )
        ),
        Prefetch(
            lookup='package_contributions',
            queryset=Package.objects.order_by(
                'name',
            )
        ),
        Prefetch(
            lookup='plugin_contributions',
            queryset=Plugin.objects.order_by(
                'name',
            )
        ),
        Prefetch(
            lookup='subplugin_contributions',
            queryset=SubPlugin.objects.order_by(
                'name',
            ).select_related(
                'plugin',
            )
        )
    ).select_related(
        'user',
    )
    serializer_class = ForumUserSerializer
