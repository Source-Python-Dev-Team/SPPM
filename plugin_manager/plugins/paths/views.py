# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

# App
from .forms import SubPluginPathCreateForm, SubPluginPathEditForm
from .models import SubPluginPath
from plugin_manager.plugins.models import Plugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginPathCreateView',
    'SubPluginPathDeleteView',
    'SubPluginPathEditView',
    'SubPluginPathListView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginPathListView(ListView):
    model = SubPluginPath
    template_name = 'plugins/paths/list.html'
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin

    def get_context_data(self, **kwargs):
        context = super(SubPluginPathListView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context

    def get_queryset(self):
        return super(SubPluginPathListView, self).get_queryset().filter(
            plugin=self.plugin,
        )


class SubPluginPathCreateView(CreateView):
    model = SubPluginPath
    form_class = SubPluginPathCreateForm
    template_name = 'plugins/paths/create.html'
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin

    def get_initial(self):
        initial = super(SubPluginPathCreateView, self).get_initial()
        initial.update({
            'plugin': self.plugin,
        })
        return initial


class SubPluginPathEditView(UpdateView):
    model = SubPluginPath
    form_class = SubPluginPathEditForm
    template_name = 'plugins/paths/edit.html'
    pk_url_kwarg = 'path_pk'
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin

    def get_context_data(self, **kwargs):
        context = super(SubPluginPathEditView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context


class SubPluginPathDeleteView(DeleteView):
    model = SubPluginPath

    def get_object(self, queryset=None):
        return SubPluginPath.objects.get(pk=self.kwargs.get('path_pk'))
