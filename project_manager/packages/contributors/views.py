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
from .forms import PackageAddContributorConfirmationForm
from project_manager.packages.mixins import RetrievePackageMixin
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
    model = ForumUser
    template_name = 'packages/contributors/add.html'
    filterset_class = ForumUserFilterSet

    def get(self, request, *args, **kwargs):
        value = super().get(request, *args, **kwargs)
        user = value.context_data['user']
        if user is not None and not value.context_data['warning_message']:
            return HttpResponseRedirect(
                reverse(
                    viewname='packages:contributors:confirm-add',
                    kwargs={
                        'slug': self.package.slug,
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
                if user == self.package.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.')
                elif user in self.package.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'package': self.package,
            'warning_message': message,
            'user': user,
        })
        return context


class PackageAddContributorConfirmationView(RetrievePackageMixin, FormView):
    form_class = PackageAddContributorConfirmationForm
    template_name = 'packages/contributors/add_confirmation.html'

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
        if self.package.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in self.package.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'package': self.package,
            'username': user.username,
            'warning_message': message,
        })
        return context

    def form_valid(self, form):
        self.package.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(self.package.get_absolute_url())
