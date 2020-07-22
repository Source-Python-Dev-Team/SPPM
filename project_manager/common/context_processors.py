"""Context processors to be added to templates."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'add_common_context_processors',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def add_common_context_processors(request):
    """Expose some settings and other information to all contexts."""
    return {
        'DOWNLOAD_URL': settings.DOWNLOAD_URL,
        'FORUM_URL': settings.FORUM_URL,
        'GITHUB_URL': settings.GITHUB_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'WIKI_URL': settings.WIKI_URL,
        'username': str(request.user),
    }
