# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# Project Imports
from plugins.models import Plugin

# App Imports
from .models import SubPlugin
from .forms import SubPluginCreateForm, SubPluginEditForm, SubPluginUpdateForm


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginCreateView',
    'SubPluginListView',
    'SubPluginUpdateView',
    'SubPluginView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class SubPluginListView(ListView):
    model = SubPlugin
    paginate_by = 20
    template_name = 'sub_plugins/list.html'

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
    template_name = 'sub_plugins/create.html'
    plugin = None

    def get_context_data(self, **kwargs):
        context = super(SubPluginCreateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'paths': self.plugin.paths.all()
        })
        return context

    def get_initial(self):
        initial = super(SubPluginCreateView, self).get_initial()
        initial.update({
            'plugin': self.get_plugin(),
        })
        return initial

    def get_plugin(self):
        self.plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self.plugin


class SubPluginEditView(UpdateView):
    model = SubPlugin
    form_class = SubPluginEditForm
    template_name = 'sub_plugins/edit.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_initial(self):
        initial = super(SubPluginEditView, self).get_initial()
        initial.update({
            'logo': '',
        })
        return initial


class SubPluginUpdateView(UpdateView):
    model = SubPlugin
    form_class = SubPluginUpdateForm
    template_name = 'sub_plugins/update.html'
    slug_url_kwarg = 'sub_plugin_slug'
    plugin = None

    def get_context_data(self, **kwargs):
        context = super(SubPluginUpdateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'sub_plugin': SubPlugin.objects.get(
                slug=context['view'].kwargs['sub_plugin_slug']),
            'paths': self.plugin.paths.all(),
        })
        return context

    def get_initial(self):
        initial = super(SubPluginUpdateView, self).get_initial()
        initial.update({
            'plugin': self.get_plugin(),
            'version': '',
            'version_notes': '',
            'zip_file': '',
        })
        return initial

    def get_plugin(self):
        self.plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self.plugin


class SubPluginView(DetailView):
    model = SubPlugin
    template_name = 'sub_plugins/view.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_context_data(self, **kwargs):
        context = super(SubPluginView, self).get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin'],
            'contributors': self.object.contributors.all(),
        })
        return context
