# =============================================================================
# >> IMPORTS
# =============================================================================
from .common.models import DownloadRequirement, VersionControlRequirement
from .games.models import Game
from .packages.models import Package, PackageImage, PackageRelease
from .plugins.models import Plugin, PluginImage, PluginRelease
from .plugins.paths.models import SubPluginPath
from .pypi.models import PyPiRequirement
from .sub_plugins.models import SubPlugin, SubPluginImage, SubPluginRelease
from .tags.models import Tag
from .users.models import ForumUser

_all_models = (
    DownloadRequirement, ForumUser, Game, Package, PackageImage,
    PackageRelease, Plugin, PluginImage, PluginRelease, PyPiRequirement,
    SubPlugin, SubPluginImage, SubPluginPath, SubPluginRelease, Tag,
    VersionControlRequirement,
)