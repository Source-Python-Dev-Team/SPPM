from django.http import Http404
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
            plugin__basename=self.kwargs['plugin_name']
        )

    def get_context_data(self, **kwargs):
        context = super(SubPluginListView, self).get_context_data(**kwargs)
        context.update({
            'plugin': Plugin.objects.get(basename=self.kwargs['plugin_name']),
            'sub_plugin_list': context['subplugin_list'],
        })
        return context


class SubPluginCreateView(CreateView):
    model = SubPlugin
    form_class = SubPluginCreateForm
    template_name = 'sub_plugins/sub_plugin_create.html'

    def get_context_data(self, **kwargs):
        context = super(SubPluginCreateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': Plugin.objects.get(basename=self.kwargs['plugin_name']),
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(SubPluginCreateView, self).get_form_kwargs()
        kwargs.update({
            'plugin_name': self.kwargs['plugin_name'],
        })
        return kwargs

    def get_success_url(self):
        return '/plugins/{0}/sub_plugins/{1}'.format(
            self.object.plugin.basename, self.object.basename)


class SubPluginView(DetailView):
    model = SubPlugin
    template_name = 'sub_plugins/sub_plugin_view.html'
    slug_url_kwarg = 'sub_plugin_name'
    slug_field = 'basename'

    def get_context_data(self, **kwargs):
        context = super(SubPluginView, self).get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin'],
        })
        return context
