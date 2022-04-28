"""User views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.views.generic import TemplateView

# App
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserView',
)


# =============================================================================
# VIEWS
# =============================================================================
class ForumUserView(TemplateView):
    """Frontend view for viewing Users."""

    template_name = 'main.html'
    http_method_names = ('get', 'options')

    def get_context_data(self, **kwargs):
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        pk = context.get('pk')
        if pk is None:
            context['title'] = 'User Listing'
        else:
            try:
                user = ForumUser.objects.select_related('user').get(forum_id=pk)
                context['title'] = user.user.username
            except ForumUser.DoesNotExist:
                context['title'] = f'Userid "{pk}" not found.'
        return context
