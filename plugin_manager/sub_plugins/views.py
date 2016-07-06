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
from plugin_manager.plugins.constants import PLUGIN_PATH
from plugin_manager.plugins.models import Plugin
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
    'SubPluginListView',
    'SubPluginEditView',
    'SubPluginReleaseDownloadView',
    'SubPluginReleaseListView',
    'SubPluginSelectGamesView',
    'SubPluginUpdateView',
    'SubPluginView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginListView(RetrieveSubPluginMixin, OrderablePaginatedListView):
    model = SubPlugin
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'sub_plugins/list.html'

    def get_queryset(self):
        return super(SubPluginListView, self).get_queryset().filter(
            plugin=self.plugin,
        )

    def get_context_data(self, **kwargs):
        context = super(SubPluginListView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'paths': self.plugin.paths.all(),
            'sub_plugin_list': context['subplugin_list'],
        })
        return context


class SubPluginCreateView(RetrieveSubPluginMixin, CreateView):
    model = SubPlugin
    form_class = SubPluginCreateForm
    template_name = 'sub_plugins/create.html'

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
            'plugin': self.plugin,
        })
        return initial

    def form_valid(self, form):
        response = super(SubPluginCreateView, self).form_valid(form)
        zip_file = ZipFile(form.cleaned_data['zip_file'])
        instance = form.instance
        requirements = get_requirements(
            zip_file,
            '{plugin_path}{plugin_basename}/{path}/{basename}/'
            'requirements.ini'.format(
                plugin_path=PLUGIN_PATH,
                plugin_basename=instance.plugin.basename,
                basename=instance.basename,
                path=form.cleaned_data['path'],
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

    def get_context_data(self, **kwargs):
        context = super(SubPluginEditView, self).get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin']
        })
        return context


class SubPluginUpdateView(RetrieveSubPluginMixin, UpdateView):
    model = SubPlugin
    form_class = SubPluginUpdateForm
    template_name = 'sub_plugins/update.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_context_data(self, **kwargs):
        context = super(SubPluginUpdateView, self).get_context_data(**kwargs)
        sub_plugin = context['subplugin']
        current_release = SubPluginRelease.objects.filter(
            sub_plugin=sub_plugin,
        ).order_by('-created')[0]
        context.update({
            'plugin': self.plugin,
            'sub_plugin': sub_plugin,
            'current_release': current_release,
            'paths': self.plugin.paths.all(),
        })
        return context

    def get_initial(self):
        initial = super(SubPluginUpdateView, self).get_initial()
        initial.update({
            'plugin': self.plugin,
            'version': '',
            'version_notes': '',
            'zip_file': '',
        })
        return initial

    def form_valid(self, form):
        response = super(SubPluginUpdateView, self).form_valid(form)
        zip_file = ZipFile(form.cleaned_data['zip_file'])
        instance = form.instance
        requirements = get_requirements(
            zip_file,
            '{plugin_path}{plugin_basename}/{path}/{basename}/'
            'requirements.ini'.format(
                plugin_path=PLUGIN_PATH,
                plugin_basename=instance.plugin.basename,
                basename=instance.basename,
                path=form.cleaned_data['path'],
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


class SubPluginSelectGamesView(UpdateView):
    model = SubPlugin
    form_class = SubPluginSelectGamesForm
    template_name = 'sub_plugins/games.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_context_data(self, **kwargs):
        context = super(
            SubPluginSelectGamesView,
            self
        ).get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin']
        })
        return context


class SubPluginView(RetrieveSubPluginMixin, DetailView):
    model = SubPlugin
    template_name = 'sub_plugins/view.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_queryset(self):
        """This is to fix a MultipleObjectsReturned error."""
        queryset = SubPlugin.objects.filter(
            pk=self.sub_plugin.pk,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SubPluginView, self).get_context_data(**kwargs)
        sub_plugin = context['subplugin']
        current_release = SubPluginRelease.objects.filter(
            sub_plugin=sub_plugin,
        ).order_by('-created')[0]
        context.update({
            'sub_plugin': sub_plugin,
            'current_release': current_release,
            'contributors': self.object.contributors.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context


class SubPluginReleaseDownloadView(DownloadMixin):
    model = SubPluginRelease
    super_model = Plugin
    sub_model = SubPlugin
    slug_url_kwarg = 'sub_plugin_slug'
    super_kwarg = 'plugin'
    sub_kwarg = 'sub_plugin'
    base_url = SUB_PLUGIN_RELEASE_URL


class SubPluginReleaseListView(RetrieveSubPluginMixin, ListView):
    model = SubPluginRelease
    template_name = 'sub_plugins/releases.html'

    def get_context_data(self, **kwargs):
        context = super(
            SubPluginReleaseListView,
            self
        ).get_context_data(**kwargs)
        context.update({
            'sub_plugin': self.sub_plugin,
        })
        return context

    def get_queryset(self):
        return SubPluginRelease.objects.filter(
            sub_plugin=self.sub_plugin,
        ).order_by('-created')
