"""Plugin contributors views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView

# 3rd-Party Django
from django_filters.views import FilterView

# App
from project_manager.plugins.mixins import RetrievePluginMixin
from project_manager.users.filtersets import ForumUserFilterSet
from project_manager.users.models import ForumUser
from .forms import PluginAddContributorConfirmationForm


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
class PluginAddContributorView(RetrievePluginMixin, FilterView):
    """View for adding a contributor to a Plugin."""

    model = ForumUser
    template_name = 'plugins/contributors/add.html'
    filterset_class = ForumUserFilterSet

    def get(self, request, *args, **kwargs):
        """Return the redirect if adding a contributor."""
        value = super().get(request, *args, **kwargs)
        user = value.context_data['user']
        if user is not None and not value.context_data['warning_message']:
            return HttpResponseRedirect(
                reverse(
                    viewname='plugins:contributors:confirm-add',
                    kwargs={
                        'slug': self.plugin.slug,
                        'id': user.id,
                    }
                )
            )
        return value

    def get_context_data(self, **kwargs):
        """Update the view's context for the template."""
        context = super().get_context_data(**kwargs)
        message = ''
        user = None
        if 'username' in self.request.GET:
            try:
                user = ForumUser.objects.get(
                    username=self.request.GET['username'])
            except ForumUser.DoesNotExist:
                pass
            else:
                if user == self.plugin.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.')
                elif user in self.plugin.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'plugin': self.plugin,
            'warning_message': message,
            'user': user,
        })
        return context


class PluginAddContributorConfirmationView(RetrievePluginMixin, FormView):
    """View for confirming adding a contributor to a Plugin."""

    form_class = PluginAddContributorConfirmationForm
    template_name = 'plugins/contributors/add_confirmation.html'

    def get_initial(self):
        """Add 'id' to the initial."""
        initial = super().get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        """Update the view's context for the template."""
        context = super().get_context_data(**kwargs)
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if self.plugin.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in self.plugin.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'plugin': self.plugin,
            'username': user.username,
            'warning_message': message,
        })
        return context

    def form_valid(self, form):
        """Add the contributors to the plugin."""
        self.plugin.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(self.plugin.get_absolute_url())
