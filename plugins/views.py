from django.views.generic import CreateView, ListView, DetailView

from .models import Plugin
from .forms import PluginCreateForm


__all__ = (
    'PluginCreateView',
    'PluginListView',
    'PluginView',
)


# Create your views here.
class PluginListView(ListView):
    model = Plugin
    paginate_by = 20
    template_name = 'plugins/plugin_list.html'


class PluginCreateView(CreateView):
    model = Plugin
    form_class = PluginCreateForm
    template_name = 'plugins/plugin_create.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class PluginView(DetailView):
    model = Plugin
    template_name = 'plugins/plugin_view.html'

    def get_context_data(self, **kwargs):
        context = super(PluginView, self).get_context_data(**kwargs)
        context.update({
            'contributors': self.object.contributors.all(),
            'paths': self.object.paths.all(),
        })
        return context
