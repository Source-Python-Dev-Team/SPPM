# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    CreateView, DetailView, FormView, ListView, UpdateView, View,
)

# 3rd-Party Django
from django_filters.views import FilterView

# App
from .constants import SUB_PLUGIN_RELEASE_URL
from .forms import (
    SubPluginAddContributorConfirmationForm, SubPluginCreateForm,
    SubPluginEditForm, SubPluginSelectGamesForm, SubPluginUpdateForm,
)
from .models import SubPlugin, SubPluginRelease
from ..common.views import OrderablePaginatedListView
from ..plugins.models import Plugin
from ..users.filtersets import ForumUserFilterSet
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAddContributorConfirmationView',
    'SubPluginAddContributorView',
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
# >> VIEW CLASSES
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


class SubPluginAddContributorView(FilterView):
    model = ForumUser
    template_name = 'sub_plugins/contributor/add.html'
    filterset_class = ForumUserFilterSet
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin

    def get_context_data(self, **kwargs):
        context = super(
            SubPluginAddContributorView,
            self
        ).get_context_data(**kwargs)
        plugin = self.plugin
        sub_plugin = SubPlugin.objects.get(
            plugin=plugin, slug=self.kwargs['sub_plugin_slug'])
        message = ''
        user = None
        if 'username' in self.request.GET:
            try:
                user = ForumUser.objects.get(
                    username=self.request.GET['username'])
            except ForumUser.DoesNotExist:
                pass
            else:
                if user == sub_plugin.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.')
                elif user in sub_plugin.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'plugin': plugin,
            'sub_plugin': sub_plugin,
            'message': message,
            'user': user,
        })
        return context


class SubPluginAddContributorConfirmationView(FormView):
    form_class = SubPluginAddContributorConfirmationForm
    template_name = 'sub_plugins/contributor/add_confirmation.html'
    _plugin = None

    @property
    def plugin(self):
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin

    def get_initial(self):
        initial = super(
            SubPluginAddContributorConfirmationView, self).get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(
            SubPluginAddContributorConfirmationView,
            self
        ).get_context_data(**kwargs)
        plugin = self.plugin
        sub_plugin = SubPlugin.objects.get(
            plugin=plugin, slug=self.kwargs['sub_plugin_slug'])
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if sub_plugin.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in sub_plugin.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'sub_plugin': sub_plugin,
            'username': ForumUser.objects.get(id=self.kwargs['id']).username,
            'message': message,
        })
        return context

    def form_valid(self, form):
        sub_plugin = SubPlugin.objects.get(
            plugin=self.plugin, slug=self.kwargs['sub_plugin_slug'])
        sub_plugin.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(sub_plugin.get_absolute_url())


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
