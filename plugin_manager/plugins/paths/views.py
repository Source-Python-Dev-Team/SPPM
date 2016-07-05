# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

# App
from .forms import SubPluginPathCreateForm, SubPluginPathEditForm
from .models import SubPluginPath
from plugin_manager.plugins.mixins import RetrievePluginMixin


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
class SubPluginPathListView(RetrievePluginMixin, ListView):
    model = SubPluginPath
    template_name = 'plugins/paths/list.html'

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


class SubPluginPathCreateView(RetrievePluginMixin, CreateView):
    model = SubPluginPath
    form_class = SubPluginPathCreateForm
    template_name = 'plugins/paths/create.html'

    def get_initial(self):
        initial = super(SubPluginPathCreateView, self).get_initial()
        initial.update({
            'plugin': self.plugin,
        })
        return initial


class SubPluginPathEditView(RetrievePluginMixin, UpdateView):
    model = SubPluginPath
    form_class = SubPluginPathEditForm
    template_name = 'plugins/paths/edit.html'
    pk_url_kwarg = 'path_pk'

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
