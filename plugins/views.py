from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Plugin
from .forms import PluginCreateForm, PluginUpdateForm


__all__ = (
    'PluginCreateView',
    'PluginListView',
    'PluginUpdateView',
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


class PluginUpdateView(UpdateView):
    model = Plugin
    form_class = PluginUpdateForm
    template_name = 'plugins/plugin_update.html'

    def get_context_data(self, **kwargs):
        context = super(PluginUpdateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': Plugin.objects.get(
                slug=context['view'].kwargs['slug'])
        })
        return context

    def get_initial(self):
        initial = super(PluginUpdateView, self).get_initial()
        initial.update({
            'version': '',
            'version_notes': '',
            'zip_file': '',
        })
        return initial


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
