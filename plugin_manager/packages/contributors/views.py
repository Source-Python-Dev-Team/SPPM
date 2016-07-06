# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.shortcuts import HttpResponseRedirect
from django.views.generic import FormView

# 3rd-Party Django
from django_filters.views import FilterView

# App
from .forms import PackageAddContributorConfirmationForm
from plugin_manager.packages.mixins import RetrievePackageMixin
from plugin_manager.packages.models import Package
from plugin_manager.users.filtersets import ForumUserFilterSet
from plugin_manager.users.models import ForumUser


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

    def get_context_data(self, **kwargs):
        context = super(
            PackageAddContributorView, self).get_context_data(**kwargs)
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
            'message': message,
            'user': user,
        })
        return context


class PackageAddContributorConfirmationView(RetrievePackageMixin, FormView):
    form_class = PackageAddContributorConfirmationForm
    template_name = 'packages/contributors/add_confirmation.html'

    def get_initial(self):
        initial = super(
            PackageAddContributorConfirmationView, self).get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(
            PackageAddContributorConfirmationView,
            self,
        ).get_context_data(**kwargs)
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if self.package.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in self.package.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'package': self.package,
            'username': ForumUser.objects.get(id=self.kwargs['id']).username,
            'message': message,
        })
        return context

    def form_valid(self, form):
        self.package.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(self.package.get_absolute_url())
