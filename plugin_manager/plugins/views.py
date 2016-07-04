# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, View,
)

# App
from .constants import PLUGIN_RELEASE_URL
from .forms import (
    PluginCreateForm, PluginEditForm, PluginSelectGamesForm, PluginUpdateForm,
)
from .models import Plugin, PluginRelease
from plugin_manager.common.views import OrderablePaginatedListView


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


class PluginReleaseDownloadView(View):
    model = PluginRelease
    full_path = None

    def dispatch(self, request, *args, **kwargs):
        self.full_path = (
            settings.MEDIA_ROOT / PLUGIN_RELEASE_URL / kwargs['slug'] /
            kwargs['zip_file']
        )
        if not self.full_path.isfile():
            raise Http404
        return super(
            PluginReleaseDownloadView,
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
        version = zip_file.split(
            '{slug}-v'.format(slug=plugin.slug), 1
        )[1].rsplit('.', 1)[0]
        PluginRelease.objects.filter(
            plugin=plugin,
            version=version
        ).update(
            download_count=F('download_count') + 1
        )
        return response


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
