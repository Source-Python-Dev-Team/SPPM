"""SubPlugin contributors views."""

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
from project_manager.sub_plugins.contributors.forms import (
    SubPluginAddContributorConfirmationForm,
)
from project_manager.sub_plugins.mixins import RetrieveSubPluginMixin
from project_manager.sub_plugins.models import SubPluginContributor
from project_manager.users.filtersets import ForumUserFilterSet
from project_manager.users.models import ForumUser


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
class SubPluginAddContributorView(RetrieveSubPluginMixin, FilterView):
    """View for adding a contributor to a SubPlugin."""

    model = ForumUser
    template_name = 'sub_plugins/contributors/add.html'
    filterset_class = ForumUserFilterSet

    def get(self, request, *args, **kwargs):
        """Return the redirect if adding a contributor."""
        value = super().get(request, *args, **kwargs)
        user = value.context_data['user']
        if user is not None and not value.context_data['warning_message']:
            return HttpResponseRedirect(
                reverse(
                    viewname='plugins:sub-plugins:contributors:confirm-add',
                    kwargs={
                        'slug': self.plugin.slug,
                        'sub_plugin_slug': self.sub_plugin.slug,
                        'forum_id': user.forum_id,
                    }
                )
            )
        return value

    def get_context_data(self, *, object_list=None, **kwargs):
        """Update the view's context for the template."""
        context = super().get_context_data(object_list=object_list, **kwargs)
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
                if forum_user == self.sub_plugin.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.'
                    )
                elif forum_user in self.sub_plugin.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'plugin': self.plugin,
            'sub_plugin': self.sub_plugin,
            'warning_message': message,
            'user': forum_user,
        })
        return context


class SubPluginAddContributorConfirmationView(
    RetrieveSubPluginMixin, FormView
):
    """View for confirming adding a contributor to a SubPlugin."""

    form_class = SubPluginAddContributorConfirmationForm
    template_name = 'sub_plugins/contributors/add_confirmation.html'

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
        if self.sub_plugin.owner == forum_user:
            message = 'is the owner and cannot be added as a contributor.'
        elif forum_user in self.sub_plugin.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'sub_plugin': self.sub_plugin,
            'username': forum_user.user.username,
            'warning_message': message,
        })
        return context

    def form_valid(self, form):
        """Add the contributors to the sub-plugin."""
        SubPluginContributor.objects.create(
            user_id=form.cleaned_data['forum_id'],
            sub_plugin=self.sub_plugin,
        )
        return HttpResponseRedirect(self.sub_plugin.get_absolute_url())
