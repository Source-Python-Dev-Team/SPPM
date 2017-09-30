""""""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework import views


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def get_view_name(view_cls, suffix=None):
    try:
        view_name = view_cls.view_name
    except AttributeError:
        return views.get_view_name(view_cls=view_cls, suffix=suffix)
    if isinstance(view_name, str):
        return view_name
    return view_name()
