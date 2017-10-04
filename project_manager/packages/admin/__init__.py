"""Package admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin
from .inlines import (
    PackageContributorInline,
    PackageGameInline,
    PackageTagInline,
)
from ..models import Package, PackageImage, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAdmin',
    'PackageImageAdmin',
    'PackageReleaseAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(Package)
class PackageAdmin(ProjectAdmin):
    """Package admin."""

    inlines = (
        PackageContributorInline,
        PackageGameInline,
        PackageTagInline,
    )


@admin.register(PackageRelease)
class PackageReleaseAdmin(admin.ModelAdmin):
    """PackageRelease admin."""

    list_display = (
        'package',
    )
    readonly_fields = (
        'package',
    )
    search_fields = (
        'package__name',
        'package__basename',
        'package__owner__user__username',
        'package__contributors__user__username',
    )


@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    """PackageImage admin."""

    list_display = (
        'package',
        'image',
    )
    readonly_fields = (
        'package',
    )
    search_fields = (
        'package__name',
        'package__basename',
    )
