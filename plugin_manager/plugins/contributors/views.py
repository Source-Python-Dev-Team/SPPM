# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.shortcuts import HttpResponseRedirect
from django.views.generic import FormView

# 3rd-Party Django
from django_filters.views import FilterView

# App
from .forms import PluginAddContributorConfirmationForm
from plugin_manager.plugins.models import Plugin
from plugin_manager.users.filtersets import ForumUserFilterSet
from plugin_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAddContributorConfirmationView',
    'PluginAddContributorView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PluginAddContributorView(FilterView):
    model = ForumUser
    template_name = 'plugins/contributors/add.html'
    filterset_class = ForumUserFilterSet

    def get_context_data(self, **kwargs):
        context = super(
            PluginAddContributorView, self).get_context_data(**kwargs)
        plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        message = ''
        user = None
        if 'username' in self.request.GET:
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
            'plugin': plugin,
            'message': message,
            'user': user,
        })
        return context


class PluginAddContributorConfirmationView(FormView):
    form_class = PluginAddContributorConfirmationForm
    template_name = 'plugins/contributors/add_confirmation.html'

    def get_initial(self):
        initial = super(
            PluginAddContributorConfirmationView, self).get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(
            PluginAddContributorConfirmationView,
            self
        ).get_context_data(**kwargs)
        plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if plugin.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in plugin.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'plugin': plugin,
            'username': ForumUser.objects.get(id=self.kwargs['id']).username,
            'message': message,
        })
        return context

    def form_valid(self, form):
        plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        plugin.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(plugin.get_absolute_url())
