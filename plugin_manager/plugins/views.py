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
    PluginAddContributorConfirmationForm,
    PluginCreateForm,
    PluginEditForm,
    PluginUpdateForm,
)
from .models import Plugin
from ..common.views import OrderablePaginatedListView
from ..users.filtersets import ForumUserFilterSet
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAddContributorConfirmationView',
    'PluginAddContributorView',
    'PluginCreateView',
    'PluginEditView',
    'PluginListView',
    'PluginUpdateView',
    'PluginView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class PluginListView(OrderablePaginatedListView):
    model = Plugin
    orderable_columns = (
        'name',
        'basename',
        'date_created',
        'date_last_updated',
    )
    orderable_columns_default = 'date_created'
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


class PluginAddContributorView(FilterView):
    model = ForumUser
    template_name = 'plugins/contributor/add.html'
    filterset_class = ForumUserFilterSet

    def get_context_data(self, **kwargs):
        context = super(
            PluginAddContributorView, self).get_context_data(**kwargs)
        message = ''
        user = None
        if 'username' in self.request.GET:
            plugin = Plugin.objects.get(slug=self.kwargs['slug'])
            try:
                user = ForumUser.objects.get(
                    username=self.request.GET['username'])
            except ForumUser.DoesNotExist:
                pass
            else:
                if user == plugin.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.')
                elif user in plugin.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'message': message,
            'user': user,
        })
        return context


class PluginAddContributorConfirmationView(FormView):
    form_class = PluginAddContributorConfirmationForm
    template_name = 'plugins/contributor/add_confirmation.html'

    def get_initial(self):
        initial = super(
            PluginAddContributorConfirmationView, self).get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if plugin.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in plugin.contributors.all():
            message = 'is already a contributor.'
        context = super(
            PluginAddContributorConfirmationView, self).get_context_data(
            **kwargs)
        context.update({
            'username': ForumUser.objects.get(id=self.kwargs['id']).username,
            'message': message,
        })
        return context

    def form_valid(self, form):
        plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        plugin.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(plugin.get_absolute_url())


class PluginUpdateView(UpdateView):
    model = Plugin
    form_class = PluginUpdateForm
    template_name = 'plugins/update.html'

    def get_context_data(self, **kwargs):
        context = super(PluginUpdateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': Plugin.objects.get(
                slug=context['view'].kwargs['slug'])
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


class PluginView(DetailView):
    model = Plugin
    template_name = 'plugins/view.html'

    def get_context_data(self, **kwargs):
        context = super(PluginView, self).get_context_data(**kwargs)
        context.update({
            'contributors': self.object.contributors.all(),
            'paths': self.object.paths.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context
