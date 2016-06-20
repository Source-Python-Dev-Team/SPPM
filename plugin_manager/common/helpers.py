# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Python
from path import Path

# Django
from django.conf import settings


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'find_image_number',
    'get_groups',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def find_image_number(directory, basename):
    """Return the next available image number."""
    path = Path(settings.MEDIA_ROOT) / 'images' / directory / basename
    current_files = [x.namebase for x in path.files()] if path.isdir() else []
    return '%04d' % (max(map(int, current_files or [0])) + 1)


def get_groups(iterable, count=3):
    if not iterable:
        return iterable
    iterable = list(iterable)
    remainder = len(iterable) % count
    iterable.extend([''] * (count - remainder))
    return zip(*(iter(iterable), ) * count)
