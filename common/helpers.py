# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Python Imports
from path import Path

# Django Imports
from django.conf import settings


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'find_image_number',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def find_image_number(directory, basename):
    """Return the next available image number."""
    path = Path(settings.MEDIA_URL) / 'images' / directory / basename
    current_files = [x.namebase for x in path.files()]
    return '%04d' % (max(map(int, current_files or [0])) + 1)
