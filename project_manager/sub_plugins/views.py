"""SubPlugin views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# App
from project_manager.common.mixins import (
    DownloadMixin,
    RequirementsParserMixin,
)
from project_manager.games.mixins import GameSpecificOrderablePaginatedListView
from project_manager.plugins.constants import PLUGIN_PATH
from project_manager.plugins.models import Plugin
from .constants import SUB_PLUGIN_RELEASE_URL
from .forms import (
    SubPluginCreateForm, SubPluginEditForm, SubPluginSelectGamesForm,
    SubPluginUpdateForm,
)
from .mixins import RetrieveSubPluginMixin
from .models import SubPlugin, SubPluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginCreateView',
    'SubPluginEditView',
    'SubPluginListView',
    'SubPluginReleaseDownloadView',
    'SubPluginReleaseListView',
    'SubPluginSelectGamesView',
    'SubPluginUpdateView',
    'SubPluginView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginListView(
    RetrieveSubPluginMixin, GameSpecificOrderablePaginatedListView
):
    """SubPlugin listing view."""

    model = SubPlugin
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'sub_plugins/list.html'

    def get_queryset(self):
        """Filter down to just the given plugin."""
        return super().get_queryset().filter(
            plugin=self.plugin,
        ).select_related('plugin')

    def get_context_data(self, **kwargs):
        """Add necessary info to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'paths': self.plugin.paths.all(),
            'sub_plugin_list': context['subplugin_list'],
        })
        return context


class SubPluginCreateView(
    RequirementsParserMixin, RetrieveSubPluginMixin, CreateView
):
    """SubPlugin creation view."""

    model = SubPlugin
    form_class = SubPluginCreateForm
    template_name = 'sub_plugins/create.html'

    def get_requirements_path(self, form):
        """Return the path for the requirements file."""
        plugin_basename = form.instance.plugin.basename
        path = form.cleaned_data['path']
        basename = form.instance.basename
        return (
            f'{PLUGIN_PATH}{plugin_basename}/{path}/{basename}/'
            'requirements.ini'
        )

    def get_context_data(self, **kwargs):
        """Add the necessary info to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'paths': self.plugin.paths.all()
        })
        return context

    def get_initial(self):
        """Add the plugin to the initial."""
        initial = super().get_initial()
        initial.update({
            'plugin': self.plugin,
        })
        return initial

    def get_form_kwargs(self):
        """Add the owner to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user.forum_user
        return kwargs


class SubPluginEditView(UpdateView):
    """Plugin field editing view."""

    model = SubPlugin
    form_class = SubPluginEditForm
    template_name = 'sub_plugins/edit.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_initial(self):
        """Add the logo to the initial."""
        initial = super().get_initial()
        initial.update({
            'logo': '',
        })
        return initial

    def get_context_data(self, **kwargs):
        """Duplicate subplugin for use in template."""
        context = super().get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin']
        })
        return context


class SubPluginUpdateView(
    RequirementsParserMixin, RetrieveSubPluginMixin, UpdateView
):
    """SubPlugin Release creation view."""

    model = SubPlugin
    form_class = SubPluginUpdateForm
    template_name = 'sub_plugins/update.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_requirements_path(self, form):
        """Return the path for the requirements file."""
        plugin_basename = form.instance.plugin.basename
        path = form.cleaned_data['path']
        basename = form.instance.basename
        return (
            f'{PLUGIN_PATH}{plugin_basename}/{path}/{basename}/'
            'requirements.ini'
        )

    def get_queryset(self):
        """Filter down to only the current sub-plugin to avoid an exception."""
        return SubPlugin.objects.filter(
            pk=self.sub_plugin.pk,
        )

    def get_context_data(self, **kwargs):
        """Add the necessary info to the context."""
        context = super().get_context_data(**kwargs)
        sub_plugin = context['subplugin']
        context.update({
            'plugin': self.plugin,
            'sub_plugin': sub_plugin,
            'current_version': self.object.current_version,
            'paths': self.plugin.paths.all(),
        })
        return context

    def get_initial(self):
        """Clear out the initial and add the plugin."""
        initial = super().get_initial()
        initial.update({
            'plugin': self.plugin,
            'version': '',
            'version_notes': '',
            'zip_file': '',
        })
        return initial


class SubPluginSelectGamesView(UpdateView):
    """SubPlugin Game selection view."""

    model = SubPlugin
    form_class = SubPluginSelectGamesForm
    template_name = 'sub_plugins/games.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_context_data(self, **kwargs):
        """Duplicate subplugin for use in template."""
        context = super().get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin']
        })
        return context


class SubPluginView(RetrieveSubPluginMixin, DetailView):
    """SubPlugin get view."""

    model = SubPlugin
    template_name = 'sub_plugins/view.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_queryset(self):
        """Filter down to only the current sub-plugin to avoid an exception."""
        return SubPlugin.objects.filter(
            pk=self.sub_plugin.pk,
        ).select_related('plugin')

    def get_context_data(self, **kwargs):
        """Add the necessary info to the context."""
        context = super().get_context_data(**kwargs)
        sub_plugin = context['subplugin']
        context.update({
            'sub_plugin': sub_plugin,
            'current_release': self.object.releases.order_by('-created')[0],
            'contributors': self.object.contributors.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context


class SubPluginReleaseDownloadView(DownloadMixin):
    """SubPlugin download view for releases."""

    model = SubPluginRelease
    super_model = Plugin
    sub_model = SubPlugin
    slug_url_kwarg = 'sub_plugin_slug'
    super_kwarg = 'plugin'
    sub_kwarg = 'sub_plugin'
    base_url = SUB_PLUGIN_RELEASE_URL


class SubPluginReleaseListView(RetrieveSubPluginMixin, ListView):
    """SubPluginRelease listing view."""

    model = SubPluginRelease
    template_name = 'sub_plugins/releases.html'

    def get_context_data(self, **kwargs):
        """Add the sub_plugin to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'sub_plugin': self.sub_plugin,
        })
        return context

    def get_queryset(self):
        """Filter down to the releases for the SubPlugin and order them."""
        return SubPluginRelease.objects.filter(
            sub_plugin=self.sub_plugin,
        ).order_by('-created')
