# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# 3rd-Party Python
from path import Path

# =============================================================================
# >> IMPORT ADMIN MODULES
# =============================================================================
for _dir in Path(__file__).parent.dirs():
    if _dir.joinpath('admin.py').isfile():
        import_module('plugin_manager.{directory}.admin'.format(
            directory=_dir.namebase,
        ))
