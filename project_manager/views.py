"""Base views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Q
from django.views.generic import TemplateView

# App
from project_manager.packages.models import Package, PackageRelease
from project_manager.plugins.models import Plugin, PluginRelease
from project_manager.sub_plugins.models import SubPlugin, SubPluginRelease
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
        package_downloads = sum(
            PackageRelease.objects.values_list(
                'download_count',
                flat=True,
            )
        )
        plugin_downloads = sum(
            PluginRelease.objects.values_list(
                'download_count',
                flat=True,
            )
        )
        sub_plugin_downloads = sum(
            SubPluginRelease.objects.values_list(
                'download_count',
                flat=True,
            )
        )
        users = ForumUser.objects.filter(
            Q(plugins__isnull=False) |
            Q(plugin_contributions__isnull=False) |
            Q(subplugins__isnull=False) |
            Q(subplugin_contributions__isnull=False) |
            Q(packages__isnull=False) |
            Q(package_contributions__isnull=False)
        ).distinct().count()
        packages = Package.objects.count()
        plugins = Plugin.objects.count()
        sub_plugins = SubPlugin.objects.count()
        context.update({
            'users': users,
            'package_count': packages,
            'plugin_count': plugins,
            'sub_plugin_count': sub_plugins,
            'total_projects': packages + plugins + sub_plugins,
            'package_downloads': package_downloads,
            'plugin_downloads': plugin_downloads,
            'sub_plugin_downloads': sub_plugin_downloads,
            'total_downloads': sum([
                package_downloads, plugin_downloads, sub_plugin_downloads,
            ])
        })
        return context
