"""Constants for use with ForumUsers."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.constants import FORUM_URL


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'FORUM_MEMBER_URL',
    'USER_USERNAME_MAX_LENGTH',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
FORUM_MEMBER_URL = FORUM_URL + 'memberlist.php?mode=viewprofile&u={user_id}'
USER_USERNAME_MAX_LENGTH = 30
