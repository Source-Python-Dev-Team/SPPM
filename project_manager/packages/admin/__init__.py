"""Package admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from copy import deepcopy

# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin, ProjectReleaseAdmin
from project_manager.packages.admin.inlines import (
    PackageContributorInline,
    PackageImageInline,
    PackageGameInline,
    PackageTagInline,
)
from project_manager.packages.models import Package, PackageRelease


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAdmin',
    'PackageReleaseAdmin',
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
    )


@admin.register(PackageRelease)
class PackageReleaseAdmin(ProjectReleaseAdmin):
    """PackageRelease admin."""

    fieldsets = deepcopy(ProjectReleaseAdmin.fieldsets)
    fieldsets[0][1]['fields'] += ('package',)
    list_display = ProjectReleaseAdmin.list_display + ('package',)
    ordering = ('package', '-created',)
    readonly_fields = ProjectReleaseAdmin.readonly_fields + ('package',)
    search_fields = ProjectReleaseAdmin.search_fields + ('package__name',)

    def get_queryset(self, request):
        """Cache 'package' for the queryset."""
        return super().get_queryset(
            request=request,
        ).select_related(
            'package',
        )
