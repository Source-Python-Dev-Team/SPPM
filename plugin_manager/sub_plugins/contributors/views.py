# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.shortcuts import HttpResponseRedirect
from django.views.generic import FormView

# 3rd-Party Django
from django_filters.views import FilterView

# App
from .forms import SubPluginAddContributorConfirmationForm
from plugin_manager.plugins.models import Plugin
from plugin_manager.sub_plugins.models import SubPlugin
from plugin_manager.users.filtersets import ForumUserFilterSet
from plugin_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAddContributorConfirmationView',
    'SubPluginAddContributorView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginAddContributorView(FilterView):
    model = ForumUser
    template_name = 'sub_plugins/contributors/add.html'
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
    template_name = 'sub_plugins/contributors/add_confirmation.html'
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
