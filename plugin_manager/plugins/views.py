# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from zipfile import ZipFile

# 3rd-Party Python
from configobj import Section

# Django
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# App
from plugin_manager.common.helpers import (
    add_download_requirement, add_package_requirement, add_pypi_requirement,
    add_vcs_requirement, flush_requirements, get_requirements,
    reset_requirements,
)
from plugin_manager.common.mixins import DownloadMixin
from plugin_manager.common.views import OrderablePaginatedListView
from .constants import PLUGIN_PATH, PLUGIN_RELEASE_URL
from .forms import (
    PluginCreateForm, PluginEditForm, PluginSelectGamesForm, PluginUpdateForm,
)
from .models import Plugin, PluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginCreateView',
    'PluginEditView',
    'PluginListView',
    'PluginReleaseDownloadView',
    'PluginReleaseListView',
    'PluginSelectGamesView',
    'PluginUpdateView',
    'PluginView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PluginListView(OrderablePaginatedListView):
    model = Plugin
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'plugins/list.html'


class PluginCreateView(CreateView):
    model = Plugin
    form_class = PluginCreateForm
    template_name = 'plugins/create.html'

    def form_valid(self, form):
        response = super(PluginCreateView, self).form_valid(form)
        zip_file = ZipFile(form.cleaned_data['zip_file'])
        instance = form.instance
        requirements = get_requirements(
            zip_file,
            '{package_path}{basename}/requirements.ini'.format(
                package_path=PLUGIN_PATH,
                basename=instance.basename,
            )
        )
        reset_requirements(instance)
        for basename in requirements.get('custom', {}):
            add_package_requirement(basename, instance)
        for basename in requirements.get('pypi', {}):
            add_pypi_requirement(basename, instance)
        for basename, url in requirements.get('vcs', {}).items():
            add_vcs_requirement(basename, url, instance)
        for basename, value in requirements.get('downloads', {}).items():
            if isinstance(value, Section):
                url = value.get('url')
                desc = value.get('desc')
            else:
                url = str(value)
                desc = ''
            add_download_requirement(basename, url, desc, instance)
        flush_requirements()
        return response


class PluginEditView(UpdateView):
    model = Plugin
    form_class = PluginEditForm
    template_name = 'plugins/edit.html'

    def get_initial(self):
        initial = super(PluginEditView, self).get_initial()
        initial.update({
            'logo': '',
        })
        return initial


class PluginUpdateView(UpdateView):
    model = Plugin
    form_class = PluginUpdateForm
    template_name = 'plugins/update.html'

    def get_context_data(self, **kwargs):
        context = super(PluginUpdateView, self).get_context_data(**kwargs)
        plugin = Plugin.objects.get(slug=context['view'].kwargs['slug'])
        current_release = PluginRelease.objects.filter(
            plugin=plugin,
        ).order_by('-created')[0]
        context.update({
            'plugin': plugin,
            'current_release': current_release,
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

    def form_valid(self, form):
        response = super(PluginUpdateView, self).form_valid(form)
        zip_file = ZipFile(form.cleaned_data['zip_file'])
        instance = form.instance
        requirements = get_requirements(
            zip_file,
            '{package_path}{basename}/requirements.ini'.format(
                package_path=PLUGIN_PATH,
                basename=instance.basename,
            )
        )
        reset_requirements(instance)
        for basename in requirements.get('custom', {}):
            add_package_requirement(basename, instance)
        for basename in requirements.get('pypi', {}):
            add_pypi_requirement(basename, instance)
        for basename, url in requirements.get('vcs', {}).items():
            add_vcs_requirement(basename, url, instance)
        for basename, value in requirements.get('downloads', {}).items():
            if isinstance(value, Section):
                url = value.get('url')
                desc = value.get('desc')
            else:
                url = str(value)
                desc = ''
            add_download_requirement(basename, url, desc, instance)
        flush_requirements()
        return response


class PluginSelectGamesView(UpdateView):
    model = Plugin
    form_class = PluginSelectGamesForm
    template_name = 'plugins/games.html'


class PluginView(DetailView):
    model = Plugin
    template_name = 'plugins/view.html'

    def get_context_data(self, **kwargs):
        context = super(PluginView, self).get_context_data(**kwargs)
        current_release = PluginRelease.objects.filter(
            plugin=self.object,
        ).order_by('-created')[0]
        context.update({
            'current_release': current_release,
            'contributors': self.object.contributors.all(),
            'paths': self.object.paths.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context


class PluginReleaseDownloadView(DownloadMixin):
    model = PluginRelease
    super_model = Plugin
    super_kwarg = 'plugin'
    base_url = PLUGIN_RELEASE_URL


class PluginReleaseListView(ListView):
    model = PluginRelease
    template_name = 'plugins/releases.html'
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(
                slug=self.kwargs['slug'],
            )
        return self._plugin

    def get_context_data(self, **kwargs):
        context = super(PluginReleaseListView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context

    def get_queryset(self):
        return PluginRelease.objects.filter(
            plugin=self.plugin,
        ).order_by('-created')
