# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import DownloadRequirement, VersionControlRequirement


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadRequirementAdmin',
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
