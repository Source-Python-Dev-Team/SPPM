"""All model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.games.models import Game
from project_manager.packages.models import (
    Package,
    PackageImage,
    PackageRelease,
)
from project_manager.plugins.models import Plugin, PluginImage, PluginRelease
from project_manager.plugins.paths.models import SubPluginPath
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginImage,
    SubPluginRelease,
)
from project_manager.tags.models import Tag
from project_manager.users.models import ForumUser
from .models import User

_all_models = (
    DownloadRequirement,
    ForumUser,
    Game,
    Package,
    PackageImage,
    PackageRelease,
    Plugin,
    PluginImage,
    PluginRelease,
    PyPiRequirement,
    SubPlugin,
    SubPluginImage,
    SubPluginPath,
    SubPluginRelease,
    User,
    Tag,
    VersionControlRequirement,
)
