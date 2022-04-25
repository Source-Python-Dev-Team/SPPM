"""API Metadata."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import PermissionDenied
from django.http.response import Http404

# Third Party Django
from rest_framework import exceptions
from rest_framework.metadata import SimpleMetadata
from rest_framework.request import clone_request


# =============================================================================
# CLASSES
# =============================================================================
class Metadata(SimpleMetadata):
    """Metadata class to show all OPTIONS available to the user."""

    def determine_actions(self, request, view):
        """Override to allow returning OPTIONS for DELETE/PATCH."""
        actions = {}
        for method in {'POST', 'DELETE', 'PATCH'} & set(view.allowed_methods):
            view.request = clone_request(request, method)
            try:
                # Test object permissions
                if method != 'POST' and hasattr(view, 'check_object_permissions'):
                    obj = view.get_object()
                    view.check_object_permissions(view.request, obj)

                # Test global permissions
                elif hasattr(view, 'check_permissions'):
                    view.check_permissions(view.request)
            except (exceptions.APIException, PermissionDenied, Http404):
                pass
            else:
                # If user has appropriate permissions for the view, include
                # appropriate metadata about the fields that should be supplied.
                serializer = view.get_serializer()
                actions[method] = self.get_serializer_info(serializer)
            finally:
                view.request = request

        return actions
