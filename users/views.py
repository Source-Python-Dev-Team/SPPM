from django.views.generic import DetailView, ListView

from .models import User


__all__ = (
    'UserListView',
    'UserView',
)


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'

    def get_queryset(self):
        return User.objects.exclude(
            plugins__isnull=True, plugin_contributions__isnull=True,
            sub_plugins__isnull=True, sub_plugin_contributions__isnull=True,
            packages__isnull=True, package_contributions__isnull=True,
        )


class UserView(DetailView):
    model = User
    template_name = 'users/user_view.html'
    slug_url_kwarg = 'user_name'
    slug_field = 'name'
