# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'FORUM_MEMBER_URL',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
FORUM_MEMBER_URL = (
    settings.FORUM_URL + 'memberlist.php?mode=viewprofile&u={user_id}'
)