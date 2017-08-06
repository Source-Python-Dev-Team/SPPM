"""SubPlugin contributors views."""

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
from project_manager.users.filtersets import ForumUserFilterSet
from project_manager.users.models import ForumUser
from .forms import SubPluginAddContributorConfirmationForm
from ..mixins import RetrieveSubPluginMixin


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
        value = super().get(
            request, *args, **kwargs
        )
        user = value.context_data['user']
        if user is not None and not value.context_data['warning_message']:
            return HttpResponseRedirect(
                reverse(
                    viewname='plugins:sub-plugins:contributors:confirm-add',
                    kwargs={
                        'slug': self.plugin.slug,
                        'sub_plugin_slug': self.sub_plugin.slug,
                        'id': user.id,
                    }
                )
            )
        return value

    def get_context_data(self, **kwargs):
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
                if user == self.sub_plugin.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.')
                elif user in self.sub_plugin.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'plugin': self.plugin,
            'sub_plugin': self.sub_plugin,
            'warning_message': message,
            'user': user,
        })
        return context


class SubPluginAddContributorConfirmationView(RetrieveSubPluginMixin, FormView):
    """View for confirming adding a contributor to a SubPlugin."""

    form_class = SubPluginAddContributorConfirmationForm
    template_name = 'sub_plugins/contributors/add_confirmation.html'

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if self.sub_plugin.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in self.sub_plugin.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'sub_plugin': self.sub_plugin,
            'username': user.username,
            'warning_message': message,
        })
        return context

    def form_valid(self, form):
        self.sub_plugin.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(self.sub_plugin.get_absolute_url())
