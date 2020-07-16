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
    'common_urls',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def common_urls(request):
    """Expose common urls to templates."""
    return {
        'DOWNLOAD_URL': settings.DOWNLOAD_URL,
        'FORUM_URL': settings.FORUM_URL,
        'GITHUB_URL': settings.GITHUB_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'WIKI_URL': settings.WIKI_URL,
        'username': str(request.user),
    }
