# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    UpdateView,
)

# 3rd-Party Django
from django_filters.views import FilterView

# App
from .forms import (
    SubPluginAddContributorConfirmationForm,
    SubPluginCreateForm,
    SubPluginEditForm,
    SubPluginUpdateForm,
)
from .models import SubPlugin
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
        'date_created',
        'date_last_updated',
    )
    orderable_columns_default = 'date_created'
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


class SubPluginAddContributorView(FilterView):
    model = ForumUser
    template_name = 'sub_plugins/contributor/add.html'
    filterset_class = ForumUserFilterSet
    plugin = None

    def get_context_data(self, **kwargs):
        context = super(
            SubPluginAddContributorView,
            self
        ).get_context_data(**kwargs)
        message = ''
        user = None
        if 'username' in self.request.GET:
            plugin = self.get_plugin()
            sub_plugin = SubPlugin.objects.get(
                plugin=plugin, slug=self.kwargs['sub_plugin_slug'])
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
            'message': message,
            'user': user,
        })
        return context

    def get_plugin(self):
        if self.plugin is None:
            self.plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self.plugin


class SubPluginAddContributorConfirmationView(FormView):
    form_class = SubPluginAddContributorConfirmationForm
    template_name = 'sub_plugins/contributor/add_confirmation.html'
    plugin = None

    def get_initial(self):
        initial = super(
            SubPluginAddContributorConfirmationView, self).get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        plugin = self.get_plugin()
        sub_plugin = SubPlugin.objects.get(
            plugin=plugin, slug=self.kwargs['sub_plugin_slug'])
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if sub_plugin.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in sub_plugin.contributors.all():
            message = 'is already a contributor.'
        context = super(
            SubPluginAddContributorConfirmationView,
            self).get_context_data(**kwargs)
        context.update({
            'username': ForumUser.objects.get(id=self.kwargs['id']).username,
            'message': message,
        })
        return context

    def form_valid(self, form):
        plugin = self.get_plugin()
        sub_plugin = SubPlugin.objects.get(
            plugin=plugin, slug=self.kwargs['sub_plugin_slug'])
        sub_plugin.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(sub_plugin.get_absolute_url())

    def get_plugin(self):
        if self.plugin is None:
            self.plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self.plugin


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
        if self.plugin is None:
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
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context
