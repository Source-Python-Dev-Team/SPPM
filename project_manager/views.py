"""Base views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

# App
from project_manager.packages.models import PackageRelease
from project_manager.plugins.models import PluginRelease
from project_manager.sub_plugins.models import SubPluginRelease
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'StatisticsView',
)


# =============================================================================
# VIEWS
# =============================================================================
class StatisticsView(TemplateView):
    """View for total Project statistics."""

    template_name = 'statistics.html'
    http_method_names = ('get', 'options')

    def get_context_data(self, **kwargs):
        """Return all statistical context data."""
        context = super().get_context_data(**kwargs)
        package_info = PackageRelease.objects.aggregate(
            download_count=Coalesce(Sum('download_count'), 0),
            project_count=Count('package', distinct=True),
        )
        plugin_info = PluginRelease.objects.aggregate(
            download_count=Coalesce(Sum('download_count'), 0),
            project_count=Count('plugin', distinct=True),
        )
        sub_plugin_info = SubPluginRelease.objects.aggregate(
            download_count=Coalesce(Sum('download_count'), 0),
            project_count=Count('sub_plugin', distinct=True),
        )
        users = ForumUser.objects.filter(
            Q(plugins__isnull=False) |
            Q(plugin_contributions__isnull=False) |
            Q(sub_plugins__isnull=False) |
            Q(sub_plugin_contributions__isnull=False) |
            Q(packages__isnull=False) |
            Q(package_contributions__isnull=False)
        ).distinct().count()
        context.update({
            'users': users,
            'package_count': package_info['project_count'],
            'plugin_count': plugin_info['project_count'],
            'sub_plugin_count': sub_plugin_info['project_count'],
            'total_projects': sum([
                package_info['project_count'],
                plugin_info['project_count'],
                sub_plugin_info['project_count'],
            ]),
            'package_downloads': package_info['download_count'],
            'plugin_downloads': plugin_info['download_count'],
            'sub_plugin_downloads': sub_plugin_info['download_count'],
            'total_downloads': sum([
                package_info['download_count'],
                plugin_info['download_count'],
                sub_plugin_info['download_count'],
            ])
        })
        return context
