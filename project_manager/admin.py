# =============================================================================
# >> IMPORTS
# =============================================================================
from .games.admin import GameAdmin
from .requirements.admin import (
    DownloadRequirementAdmin,
    PyPiRequirementAdmin,
    VersionControlRequirementAdmin,
)
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
