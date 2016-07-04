# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import TemplateView

# App
from .packages.models import Package, PackageRelease
from .plugins.models import Plugin, PluginRelease
from .sub_plugins.models import SubPlugin, SubPluginRelease
from .users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'StatisticsView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        package_downloads = sum(
            PackageRelease.objects.all().values_list(
                'download_count',
                flat=True,
            )
        )
        plugin_downloads = sum(
            PluginRelease.objects.all().values_list(
                'download_count',
                flat=True,
            )
        )
        sub_plugin_downloads = sum(
            SubPluginRelease.objects.all().values_list(
                'download_count',
                flat=True,
            )
        )
        context.update({
            'users': ForumUser.objects.exclude(
                plugins__isnull=True, plugin_contributions__isnull=True,
                sub_plugins__isnull=True, sub_plugin_contributions__isnull=True,
                packages__isnull=True, package_contributions__isnull=True,
            ).count(),
            'package_count': Package.objects.count(),
            'plugin_count': Plugin.objects.count(),
            'sub_plugin_count': SubPlugin.objects.count(),
            'package_downloads': package_downloads,
            'plugin_downloads': plugin_downloads,
            'sub_plugin_downloads': sub_plugin_downloads,
            'total_downloads': sum([
                package_downloads, plugin_downloads, sub_plugin_downloads,
            ])
        })
        return context
