"""Constants for use with ForumUsers."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.conf import settings


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'FORUM_MEMBER_URL',
    'USER_EMAIL_MAX_LENGTH',
    'USER_USERNAME_MAX_LENGTH',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
FORUM_MEMBER_URL = (
    settings.FORUM_URL + 'memberlist.php?mode=viewprofile&u={user_id}'
)
USER_USERNAME_MAX_LENGTH = 30
USER_EMAIL_MAX_LENGTH = 256
