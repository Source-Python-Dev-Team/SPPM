"""Plugin contributors views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView

# 3rd-Party Django
from django_filters.views import FilterView

# App
from project_manager.users.filtersets import ForumUserFilterSet
from project_manager.users.models import ForumUser
from .forms import PluginAddContributorConfirmationForm
from ..mixins import RetrievePluginMixin
from ..models import PluginContributor


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
                        'forum_id': user.forum_id,
                    }
                )
            )
        return value

    def get_context_data(self, **kwargs):
        """Update the view's context for the template."""
        context = super().get_context_data(**kwargs)
        message = ''
        forum_user = None
        if 'username' in self.request.GET:
            try:
                forum_user = ForumUser.objects.get(
                    user__username=self.request.GET['username'],
                )
            except ForumUser.DoesNotExist:
                pass
            else:
                if forum_user == self.plugin.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.'
                    )
                elif forum_user in self.plugin.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'plugin': self.plugin,
            'warning_message': message,
            'user': forum_user,
        })
        return context


class PluginAddContributorConfirmationView(RetrievePluginMixin, FormView):
    """View for confirming adding a contributor to a Plugin."""

    form_class = PluginAddContributorConfirmationForm
    template_name = 'plugins/contributors/add_confirmation.html'

    def get_initial(self):
        """Add 'forum_id' to the initial."""
        initial = super().get_initial()
        initial.update({
            'forum_id': self.kwargs['forum_id']
        })
        return initial

    def get_context_data(self, **kwargs):
        """Update the view's context for the template."""
        context = super().get_context_data(**kwargs)
        forum_user = ForumUser.objects.get(forum_id=self.kwargs['forum_id'])
        message = None
        if self.plugin.owner == forum_user:
            message = 'is the owner and cannot be added as a contributor.'
        elif forum_user in self.plugin.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'plugin': self.plugin,
            'username': forum_user.user.username,
            'warning_message': message,
        })
        return context

    def form_valid(self, form):
        """Add the contributors to the plugin."""
        PluginContributor.objects.create(
            user_id=form.cleaned_data['forum_id'],
            plugin=self.plugin,
        )
        return HttpResponseRedirect(self.plugin.get_absolute_url())
