"""Package contributors views."""

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
from project_manager.packages.contributors.forms import (
    PackageAddContributorConfirmationForm,
)
from project_manager.packages.mixins import RetrievePackageMixin
from project_manager.packages.models import PackageContributor
from project_manager.users.filtersets import ForumUserFilterSet
from project_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAddContributorConfirmationView',
    'PackageAddContributorView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PackageAddContributorView(RetrievePackageMixin, FilterView):
    """View for adding a contributor to a Package."""

    model = ForumUser
    template_name = 'packages/contributors/add.html'
    filterset_class = ForumUserFilterSet

    def get(self, request, *args, **kwargs):
        """Return the redirect if adding a contributor."""
        value = super().get(request, *args, **kwargs)
        user = value.context_data['user']
        if user is not None and not value.context_data['warning_message']:
            return HttpResponseRedirect(
                reverse(
                    viewname='packages:contributors:confirm-add',
                    kwargs={
                        'slug': self.package.slug,
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
                if forum_user == self.package.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.'
                    )
                elif forum_user in self.package.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'package': self.package,
            'warning_message': message,
            'user': forum_user,
        })
        return context


class PackageAddContributorConfirmationView(RetrievePackageMixin, FormView):
    """View for confirming adding a contributor to a Package."""

    form_class = PackageAddContributorConfirmationForm
    template_name = 'packages/contributors/add_confirmation.html'

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
        if self.package.owner == forum_user:
            message = 'is the owner and cannot be added as a contributor.'
        elif forum_user in self.package.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'package': self.package,
            'username': forum_user.user.username,
            'warning_message': message,
        })
        return context

    def form_valid(self, form):
        """Add the contributors to the package."""
        PackageContributor.objects.create(
            user_id=form.cleaned_data['forum_id'],
            package=self.package,
        )
        return HttpResponseRedirect(self.package.get_absolute_url())
