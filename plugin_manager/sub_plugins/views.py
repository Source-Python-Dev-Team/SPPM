# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from zipfile import ZipFile

# 3rd-Party Python
from configobj import Section

# Django
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, View,
)

# App
from plugin_manager.common.helpers import (
    add_download_requirement, add_package_requirement, add_pypi_requirement,
    add_vcs_requirement, flush_requirements, get_requirements,
    reset_requirements,
)
from plugin_manager.common.views import OrderablePaginatedListView
from plugin_manager.plugins.constants import PLUGIN_PATH
from plugin_manager.plugins.models import Plugin
from .constants import SUB_PLUGIN_RELEASE_URL
from .forms import (
    SubPluginCreateForm, SubPluginEditForm, SubPluginSelectGamesForm,
    SubPluginUpdateForm,
)
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
class SubPluginListView(OrderablePaginatedListView):
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
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin

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


class SubPluginUpdateView(UpdateView):
    model = SubPlugin
    form_class = SubPluginUpdateForm
    template_name = 'sub_plugins/update.html'
    slug_url_kwarg = 'sub_plugin_slug'
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin

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


class SubPluginView(DetailView):
    model = SubPlugin
    template_name = 'sub_plugins/view.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_queryset(self):
        """This is to fix a MultipleObjectsReturned error."""
        plugin = Plugin.objects.get(
            slug=self.kwargs['slug'],
        )
        queryset = SubPlugin.objects.filter(
            plugin=plugin,
            slug=self.kwargs['sub_plugin_slug'],
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


class SubPluginReleaseDownloadView(View):
    model = SubPluginRelease
    full_path = None

    def dispatch(self, request, *args, **kwargs):
        self.full_path = (
            settings.MEDIA_ROOT / SUB_PLUGIN_RELEASE_URL / kwargs['slug'] /
            kwargs['sub_plugin_slug'] / kwargs['zip_file']
        )
        if not self.full_path.isfile():
            raise Http404
        return super(
            SubPluginReleaseDownloadView,
            self
        ).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        zip_file = kwargs['zip_file']
        with self.full_path.open('rb') as open_file:
            response = HttpResponse(
                content=open_file.read(),
                content_type='application/force-download',
            )
        response['Content-Disposition'] = (
            'attachment: filename={filename}'.format(
                filename=zip_file,
            )
        )
        plugin = Plugin.objects.get(slug=kwargs['slug'])
        sub_plugin = SubPlugin.objects.get(
            plugin=plugin,
            slug=kwargs['sub_plugin_slug'],
        )
        version = zip_file.split(
            '{slug}-v'.format(slug=sub_plugin.slug), 1
        )[1].rsplit('.', 1)[0]
        SubPluginRelease.objects.filter(
            sub_plugin=sub_plugin,
            version=version
        ).update(
            download_count=F('download_count') + 1
        )
        return response


class SubPluginReleaseListView(ListView):
    model = SubPluginRelease
    template_name = 'sub_plugins/releases.html'
    _sub_plugin = None

    @property
    def sub_plugin(self):
        if self._sub_plugin is None:
            plugin = Plugin.objects.get(
                slug=self.kwargs['slug'],
            )
            self._sub_plugin = SubPlugin.objects.get(
                plugin=plugin,
                slug=self.kwargs['sub_plugin_slug'],
            )
        return self._sub_plugin

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
