"""Requirement app config."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.apps import AppConfig


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'RequirementConfig',
)


# =============================================================================
# APPLICATION CONFIG
# =============================================================================
class RequirementConfig(AppConfig):
    """Requirement app config."""

    name = 'requirements'
    verbose_name = 'Requirements'