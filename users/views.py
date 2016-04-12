# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.views.generic import DetailView, ListView

# App Imports
from .models import User


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'UserListView',
    'UserView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class UserListView(ListView):
    model = User
    template_name = 'users/list.html'

    def get_queryset(self):
        return User.objects.exclude(
            plugins__isnull=True, plugin_contributions__isnull=True,
            sub_plugins__isnull=True, sub_plugin_contributions__isnull=True,
            packages__isnull=True, package_contributions__isnull=True,
        )


class UserView(DetailView):
    model = User
    template_name = 'users/view.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context.update({
            'plugins': self.object.plugins.all(),
            'sub_plugins': self.object.sub_plugins.all(),
            'packages': self.object.packages.all(),
            'plugin_contributions': self.object.plugin_contributions.all(),
            'sub_plugin_contributions': self.object.sub_plugin_contributions.all(),
            'package_contributions': self.object.package_contributions.all(),
        })
        return context
