# =============================================================================
# >> IMPORTS
# =============================================================================
from .games.models import Game
from .packages.models import Package, PackageImage, PackageRelease
from .plugins.models import Plugin, PluginImage, PluginRelease, SubPluginPath
from .pypi.models import PyPiRequirement
from .sub_plugins.models import SubPlugin, SubPluginImage, SubPluginRelease
from .tags.models import Tag
from .users.models import ForumUser

_all_models = (
    ForumUser, Game, Package, PackageImage, PackageRelease, Plugin,
    PluginImage, PluginRelease, PyPiRequirement, SubPlugin, SubPluginImage,
    SubPluginPath, SubPluginRelease, Tag,
)
