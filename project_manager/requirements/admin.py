# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import (
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
    list_display = (
        'name',
        'url',
        'description',
    )
    search_fields = (
        'name',
        'url',
    )


@admin.register(PyPiRequirement)
class PyPiRequirementAdmin(admin.ModelAdmin):
    exclude = (
        'slug',
    )
    readonly_fields = (
        'name',
    )


@admin.register(VersionControlRequirement)
class VersionControlRequirementAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
    )
    search_fields = (
        'name',
        'url',
    )
