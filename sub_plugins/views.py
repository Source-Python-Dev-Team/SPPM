from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, DetailView

from plugins.models import Plugin
from .models import SubPlugin
from .forms import SubPluginCreateForm


__all__ = (
    'SubPluginCreateView',
    'SubPluginListView',
    'SubPluginView',
)


# Create your views here.
class SubPluginListView(ListView):
    model = SubPlugin
    paginate_by = 20
    template_name = 'sub_plugins/sub_plugin_list.html'

    def get_queryset(self):
        return super(SubPluginListView, self).get_queryset().filter(
            plugin__slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super(SubPluginListView, self).get_context_data(**kwargs)
        plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        context.update({
            'plugin': plugin,
            'paths': plugin.paths.all(),
            'sub_plugin_list': context['subplugin_list'],
        })
        return context


class SubPluginCreateView(CreateView):
    model = SubPlugin
    form_class = SubPluginCreateForm
    template_name = 'sub_plugins/sub_plugin_create.html'
    plugin = None

    def get_context_data(self, **kwargs):
        context = super(SubPluginCreateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'paths': self.plugin.paths.all()
        })
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_initial(self):
        initial = super(SubPluginCreateView, self).get_initial()
        initial.update({
            'plugin': self.get_plugin(),
        })
        return initial

    def get_plugin(self):
        self.plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self.plugin


class SubPluginView(DetailView):
    model = SubPlugin
    template_name = 'sub_plugins/sub_plugin_view.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_context_data(self, **kwargs):
        context = super(SubPluginView, self).get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin'],
            'contributors': self.object.contributors.all(),
        })
        return context
