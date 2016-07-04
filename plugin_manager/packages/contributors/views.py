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
class PackageAddContributorView(FilterView):
    model = ForumUser
    template_name = 'packages/contributors/add.html'
    filterset_class = ForumUserFilterSet

    def get_context_data(self, **kwargs):
        context = super(
            PackageAddContributorView, self).get_context_data(**kwargs)
        package = Package.objects.get(slug=self.kwargs['slug'])
        message = ''
        user = None
        if 'username' in self.request.GET:
            try:
                user = ForumUser.objects.get(
                    username=self.request.GET['username'])
            except ForumUser.DoesNotExist:
                pass
            else:
                if user == package.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.')
                elif user in package.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'package': package,
            'message': message,
            'user': user,
        })
        return context


class PackageAddContributorConfirmationView(FormView):
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
        package = Package.objects.get(slug=self.kwargs['slug'])
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if package.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in package.contributors.all():
            message = 'is already a contributor.'
        context.update({
            'package': package,
            'username': ForumUser.objects.get(id=self.kwargs['id']).username,
            'message': message,
        })
        return context

    def form_valid(self, form):
        package = Package.objects.get(slug=self.kwargs['slug'])
        package.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(package.get_absolute_url())
