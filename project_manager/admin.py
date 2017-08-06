# =============================================================================
# >> IMPORTS
# =============================================================================
from .games.admin import GameAdmin
from .packages.admin import (
    PackageAdmin,
    PackageImageAdmin,
    PackageReleaseAdmin,
)
from .plugins.admin import PluginAdmin, PluginImageAdmin, PluginReleaseAdmin
from .plugins.paths.admin import SubPluginPathAdmin
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
    DownloadRequirementAdmin,
    ForumUserAdmin,
    GameAdmin,
    PackageAdmin,
    PackageImageAdmin,
    PackageReleaseAdmin,
    PluginAdmin,
    PluginImageAdmin,
    PluginReleaseAdmin,
    PyPiRequirementAdmin,
    SubPluginAdmin,
    SubPluginImageAdmin,
    SubPluginPathAdmin,
    SubPluginReleaseAdmin,
    TagAdmin,
    VersionControlRequirementAdmin,
)
