# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import TemplateView

# App
from .packages.models import Package
from .plugins.models import Plugin
from .sub_plugins.models import SubPlugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'StatisticsView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        context.update({
            'package_count': Package.objects.count(),
            'plugin_count': Plugin.objects.count(),
            'sub_plugin_count': SubPlugin.objects.count(),
        })
        return context
