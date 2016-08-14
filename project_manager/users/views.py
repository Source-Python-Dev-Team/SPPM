# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.http.response import Http404
from django.views.generic import DetailView

# App
from project_manager.common.views import PaginatedListView
from .models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'UserListView',
    'UserView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class UserListView(PaginatedListView):
    model = ForumUser
    paginate_by = 40
    template_name = 'users/list.html'

    def get_queryset(self):
        return ForumUser.objects.exclude(
            plugins__isnull=True, plugin_contributions__isnull=True,
            sub_plugins__isnull=True, sub_plugin_contributions__isnull=True,
            packages__isnull=True, package_contributions__isnull=True,
        )


class UserView(DetailView):
    model = ForumUser
    template_name = 'users/view.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context.update({
            'plugins': self.object.plugins.all(),
            'sub_plugins': (
                self.object.sub_plugins.all().select_related(
                    'plugin',
                )
            ),
            'packages': self.object.packages.all(),
            'plugin_contributions': self.object.plugin_contributions.all(),
            'sub_plugin_contributions': (
                self.object.sub_plugin_contributions.all().select_related(
                    'plugin',
                )
            ),
            'package_contributions': self.object.package_contributions.all(),
        })
        return context

    def get_object(self, queryset=None):
        try:
            forum_user = super(UserView, self).get_object(queryset)
        except Http404:

            # TODO: Get user from forum
            from random import choice, randint
            import string
            all_chars = string.ascii_letters + string.digits + '-._'
            forum_user = ForumUser.objects.create(
                username=''.join(choice(all_chars) for x in range(
                    randint(4, 12))),
                id=self.kwargs['pk'],
            )
        return forum_user
