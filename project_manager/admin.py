# =============================================================================
# >> IMPORTS
# =============================================================================
from .common.admin import (
    DownloadRequirementAdmin, VersionControlRequirementAdmin,
)
from .games.admin import GameAdmin
from .pypi.admin import PyPiRequirementAdmin
from .sub_plugins.admin import (
    SubPluginAdmin, SubPluginImageAdmin, SubPluginReleaseAdmin,
)
from .tags.admin import TagAdmin
from .users.admin import ForumUserAdmin

_all_admins = (
    DownloadRequirementAdmin, ForumUserAdmin, GameAdmin, PyPiRequirementAdmin,
    SubPluginAdmin, SubPluginImageAdmin, SubPluginReleaseAdmin, TagAdmin,
    VersionControlRequirementAdmin,
)
