# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
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
        'FORUM_URL': settings.FORUM_URL,
        'WIKI_URL': settings.WIKI_URL,
        'GITHUB_URL': settings.GITHUB_URL,
        'MEDIA_URL': settings.MEDIA_URL,
    }
