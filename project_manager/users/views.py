"""User views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.http.response import Http404
from django.views.generic import DetailView

# App
from project_manager.common.views import PaginatedListView
from project_manager.users.models import ForumUser


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
    """User listing view."""

    model = ForumUser
    paginate_by = 40
    template_name = 'users/list.html'

    def get_queryset(self):
        """Filter out any ForumUsers with no contributions."""
        return ForumUser.objects.exclude(
            plugins__isnull=True, plugin_contributions__isnull=True,
            subplugins__isnull=True, subplugin_contributions__isnull=True,
            packages__isnull=True, package_contributions__isnull=True,
        )


class UserView(DetailView):
    """User get view."""

    model = ForumUser
    template_name = 'users/view.html'

    def get_context_data(self, **kwargs):
        """Add all the ForumUser's contributions to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugins': self.object.plugins.all(),
            'sub_plugins': (
                self.object.subplugins.all().select_related(
                    'plugin',
                )
            ),
            'packages': self.object.packages.all(),
            'plugin_contributions': self.object.plugin_contributions.all(),
            'sub_plugin_contributions': (
                self.object.subplugin_contributions.all().select_related(
                    'plugin',
                )
            ),
            'package_contributions': self.object.package_contributions.all(),
        })
        return context

    def get_object(self, queryset=None):
        """Retrieve the User from the forum if not already a known member."""
        try:
            forum_user = super().get_object(queryset)
        except Http404:

            # TODO: Get user from forum
            from random import choice, randint
            import string
            all_chars = string.ascii_letters + string.digits + '-._'
            forum_user = ForumUser.objects.create(
                username=''.join(
                    choice(all_chars) for _ in range(randint(4, 12))
                ),
                forum_id=self.kwargs['forum_id'],
            )
        return forum_user
