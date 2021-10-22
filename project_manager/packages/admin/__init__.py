"""Package admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin
from project_manager.packages.admin.inlines import (
    PackageContributorInline,
    PackageImageInline,
    PackageGameInline,
    PackageReleaseInline,
    PackageTagInline,
)
from project_manager.packages.models import Package


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAdmin',
)


# =============================================================================
# ADMINS
# =============================================================================
@admin.register(Package)
class PackageAdmin(ProjectAdmin):
    """Package admin."""

    inlines = (
        PackageContributorInline,
        PackageGameInline,
        PackageImageInline,
        PackageTagInline,
        PackageReleaseInline,
    )
