# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# 3rd-Party Python
from path import Path

# Django
from django.conf import settings


# =============================================================================
# >> IMPORT ADMIN MODULES
# =============================================================================
for _file in Path(__file__).parent.walkfiles('admin.py'):
    import_module(
        _file.replace(
            settings.BASE_DIR,
            ''
        )[1:~2].replace('/', '.').replace('\\', '.')
    )
