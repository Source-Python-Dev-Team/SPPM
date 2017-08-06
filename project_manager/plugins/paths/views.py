"""SubPluginPath views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

# App
from project_manager.plugins.mixins import RetrievePluginMixin
from .forms import SubPluginPathCreateForm, SubPluginPathEditForm
from .models import SubPluginPath


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
    """SubPluginPath listing view."""

    model = SubPluginPath
    template_name = 'plugins/paths/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            plugin=self.plugin,
        )


class SubPluginPathCreateView(RetrievePluginMixin, CreateView):
    """SubPluginPath creation view."""

    model = SubPluginPath
    form_class = SubPluginPathCreateForm
    template_name = 'plugins/paths/create.html'

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'plugin': self.plugin,
        })
        return initial


class SubPluginPathEditView(RetrievePluginMixin, UpdateView):
    """SubPluginPath update view."""

    model = SubPluginPath
    form_class = SubPluginPathEditForm
    template_name = 'plugins/paths/edit.html'
    pk_url_kwarg = 'path_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context


class SubPluginPathDeleteView(DeleteView):
    """SubPluginPath deletion view."""

    model = SubPluginPath

    def get_object(self, queryset=None):
        return SubPluginPath.objects.get(pk=self.kwargs.get('path_pk'))
