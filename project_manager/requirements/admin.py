"""Requirement admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadRequirementAdmin',
    'PyPiRequirementAdmin',
    'VersionControlRequirementAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(DownloadRequirement)
class DownloadRequirementAdmin(admin.ModelAdmin):
    """DownloadRequirement admin."""

    list_display = (
        'url',
    )
    search_fields = (
        'url',
    )


@admin.register(PyPiRequirement)
class PyPiRequirementAdmin(admin.ModelAdmin):
    """PyPiRequirement admin."""

    exclude = (
        'slug',
    )
    readonly_fields = (
        'name',
    )


@admin.register(VersionControlRequirement)
class VersionControlRequirementAdmin(admin.ModelAdmin):
    """VersionControlRequirement admin."""

    list_display = (
        'url',
    )
    search_fields = (
        'url',
    )
