"""User API views."""

# =============================================================================
# IMPORTS
# =============================================================================
#  Django
from django.db.models import Count, F, Prefetch

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

# App
from project_manager.sub_plugins.models import SubPlugin
from users.api.filtersets import ForumUserFilterSet
from users.api.ordering import ForumUserOrderingFilter
from users.api.serializers import ForumUserListSerializer, ForumUserRetrieveSerializer
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
    *  **username** (descending) or **-username** (ascending)

        ####Example:
        `?ordering=forum_id`

        `?ordering=-username`
    """

    filter_backends = (ForumUserOrderingFilter, DjangoFilterBackend)
    filterset_class = ForumUserFilterSet
    http_method_names = ('get', 'options')
    ordering = ('username',)
    ordering_fields = ('forum_id', 'username')
    queryset = ForumUser.objects.select_related('user')
    serializer_class = ForumUserRetrieveSerializer

    def get_serializer_class(self):
        """Return the correct serializer based on the action."""
        if self.action == 'retrieve':
            return ForumUserRetrieveSerializer

        return ForumUserListSerializer

    def get_queryset(self):
        """Add prefetching or annotation based on the action."""
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            return queryset.prefetch_related(
                Prefetch(
                    lookup='sub_plugins',
                    queryset=SubPlugin.objects.select_related(
                        'plugin',
                    ).order_by(
                        'name',
                    ),
                ),
                Prefetch(
                    lookup='sub_plugin_contributions',
                    queryset=SubPlugin.objects.select_related(
                        'plugin',
                    ).order_by(
                        'name',
                    ),
                ),
            )

        return queryset.annotate(
            package_count=Count('packages', distinct=True),
            package_contribution_count=Count('package_contributions', distinct=True),
            plugin_count=Count('plugins', distinct=True),
            plugin_contribution_count=Count('plugin_contributions', distinct=True),
            sub_plugin_count=Count('sub_plugins', distinct=True),
            sub_plugin_contribution_count=Count('sub_plugin_contributions', distinct=True),
            project_count=F('package_count') + F('plugin_count') + F('sub_plugin_count'),
            project_contribution_count=(
                F('package_contribution_count') +
                F('plugin_contribution_count') +
                F('sub_plugin_contribution_count')
            ),
            total_count=F('project_count') + F('project_contribution_count'),
        )
