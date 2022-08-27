"""Context processors to be added to templates."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.conf import settings

# App
from project_manager.constants import (
    DOWNLOAD_URL,
    FORUM_URL,
    GITHUB_URL,
    WIKI_URL,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'add_common_context_processors',
)


# =============================================================================
# FUNCTIONS
# =============================================================================
def add_common_context_processors(request):
    """Expose some settings and other information to all contexts."""
    return {
        'DOWNLOAD_URL': DOWNLOAD_URL,
        'FORUM_URL': FORUM_URL,
        'GITHUB_URL': GITHUB_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'WIKI_URL': WIKI_URL,
        'username': str(request.user),
        'user_authenticated': request.user.is_authenticated,
    }
